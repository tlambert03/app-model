from __future__ import annotations

import contextlib
import os
import sys
from typing import TYPE_CHECKING, ClassVar, Iterable, MutableMapping

import in_n_out as ino
from psygnal import Signal

from .expressions import Context, app_model_context
from .registries import (
    CommandsRegistry,
    KeyBindingsRegistry,
    MenusRegistry,
    register_action,
)

if TYPE_CHECKING:
    from .types import Action
    from .types._constants import DisposeCallable


class Application:
    """Full application model.

    This is the top level object that comprises all of the registries, and other
    app-namespace specific objects.

    Parameters
    ----------
    name : str
        A name for this application.
    raise_synchronous_exceptions : bool
        Whether to raise exceptions that occur while executing commands synchronously,
        by default False. This is settable after instantiation, and can also be
        controlled per execution by calling `result.result()` on the future object
        returned from the `execute_command` method.
    commands_reg_class : type[CommandsRegistry]
        (Optionally) override the class to use when creating the CommandsRegistry
    menus_reg_class : type[MenusRegistry]
        (Optionally) override the class to use when creating the MenusRegistry
    keybindings_reg_class : type[KeyBindingsRegistry]
        (Optionally) override the class to use when creating the KeyBindingsRegistry
    injection_store_class : type[ino.Store]
        (Optionally) override the class to use when creating the injection Store
    context : Context | MutableMapping | None
        (Optionally) provide a context to use for this application. If a
        `MutableMapping` is provided, it will be used to create a `Context` instance.
        If `None` (the default), a new `Context` instance will be created.

    Attributes
    ----------
    commands : CommandsRegistry
        The Commands Registry for this application.
    menus : MenusRegistry
        The Menus Registry for this application.
    keybindings : KeyBindingsRegistry
        The KeyBindings Registry for this application.
    injection_store : in_n_out.Store
        The Injection Store for this application.
    context : Context
        The Context for this application.
    """

    destroyed = Signal(str)
    _instances: ClassVar[dict[str, Application]] = {}

    def __init__(
        self,
        name: str,
        *,
        raise_synchronous_exceptions: bool = False,
        commands_reg_class: type[CommandsRegistry] = CommandsRegistry,
        menus_reg_class: type[MenusRegistry] = MenusRegistry,
        keybindings_reg_class: type[KeyBindingsRegistry] = KeyBindingsRegistry,
        injection_store_class: type[ino.Store] = ino.Store,
        context: Context | MutableMapping | None = None,
    ) -> None:
        self._name = name
        if name in Application._instances:
            raise ValueError(
                f"Application {name!r} already exists. Retrieve it with "
                f"`Application.get_or_create({name!r})`."
            )
        Application._instances[name] = self

        if context is None:
            context = Context()
        elif isinstance(context, MutableMapping):
            context = Context(context)
        if not isinstance(context, Context):
            raise TypeError(
                f"context must be a Context or MutableMapping, got {type(context)}"
            )
        self._context = context
        self._context.update(app_model_context())

        self._context["is_linux"] = sys.platform.startswith("linux")
        self._context["is_mac"] = sys.platform == "darwin"
        self._context["is_windows"] = os.name == "nt"

        self._injection_store = injection_store_class.create(name)
        self._commands = commands_reg_class(
            self.injection_store,
            raise_synchronous_exceptions=raise_synchronous_exceptions,
        )
        self._menus = menus_reg_class()
        self._keybindings = keybindings_reg_class()

        self.injection_store.on_unannotated_required_args = "ignore"

        self._disposers: list[tuple[str, DisposeCallable]] = []

    @property
    def raise_synchronous_exceptions(self) -> bool:
        """Whether to raise synchronous exceptions."""
        return self._commands._raise_synchronous_exceptions

    @raise_synchronous_exceptions.setter
    def raise_synchronous_exceptions(self, value: bool) -> None:
        self._commands._raise_synchronous_exceptions = value

    @property
    def commands(self) -> CommandsRegistry:
        """Return the [`CommandsRegistry`][app_model.registries.CommandsRegistry]."""
        return self._commands

    @property
    def menus(self) -> MenusRegistry:
        """Return the [`MenusRegistry`][app_model.registries.MenusRegistry]."""
        return self._menus

    @property
    def keybindings(self) -> KeyBindingsRegistry:
        """Return the [`KeyBindingsRegistry`][app_model.registries.KeyBindingsRegistry]."""  # noqa E501
        return self._keybindings

    @property
    def injection_store(self) -> ino.Store:
        """Return the `in_n_out.Store` instance associated with this `Application`."""
        return self._injection_store

    @property
    def context(self) -> Context:
        """Return the [`Context`][app_model.expressions.Context] for this application."""  # noqa E501
        return self._context

    @classmethod
    def get_or_create(cls, name: str) -> Application:
        """Get app named `name` or create and return a new one if it doesn't exist."""
        return cls._instances[name] if name in cls._instances else cls(name)

    @classmethod
    def get_app(cls, name: str) -> Application | None:
        """Return app named `name` or None if it doesn't exist."""
        return cls._instances.get(name)

    @classmethod
    def destroy(cls, name: str) -> None:
        """Destroy the `Application` named `name`.

        This will call [`dispose()`][app_model.Application.dispose], destroy the
        injection store, and remove the application from the list of stored
        application names (allowing the name to be reused).

        Parameters
        ----------
        name : str
            The name of the application to destroy.  If the application does not exist,
            this is a no-op.
        """
        if name not in cls._instances:
            return  # pragma: no cover
        app = cls._instances.pop(name)
        app.dispose()
        app.injection_store.destroy(name)
        app.destroyed.emit(app.name)

    @property
    def name(self) -> str:
        """Return the name of this `Application`."""
        return self._name

    def __repr__(self) -> str:
        return f"Application({self.name!r})"

    def dispose(self) -> None:
        """Dispose this `Application`.

        This clears all registries by calling all disposer functions.
        """
        while self._disposers:
            with contextlib.suppress(Exception):
                self._disposers.pop()[1]()

    def register_action(self, action: Action) -> DisposeCallable:
        """Register [`Action`][app_model.Action] instance with this application.

        An [`Action`][app_model.Action] is the complete representation of a command,
        including information about where and whether it appears in menus and optional
        keybinding rules.

        Parameters
        ----------
        action : Action
            The action to register.

        Returns
        -------
        Callable[[], None]
            A function that may be called with no arguments to undo the registration
            of `action`.
        """
        return register_action(self, id_or_action=action)

    def register_actions(self, actions: Iterable[Action]) -> DisposeCallable:
        """Register multiple [`Action`][app_model.Action] instances with this app.

        Parameters
        ----------
        actions : Iterable[Action]
            An iterable of actions to register.

        Returns
        -------
        Callable[[], None]
            A function that may be called with no arguments to undo the registration
            of `actions`.
        """
        d = [self.register_action(action) for action in actions]

        def _dispose() -> None:
            while d:
                d.pop()()

        return _dispose
