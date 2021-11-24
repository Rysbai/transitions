from ..core import Condition, Event, EventData, Machine, State, Transition
from .nesting import HierarchicalMachine, NestedEvent, NestedState, NestedTransition
from typing import Any, Optional, List, Type, Dict, Deque, Callable, Union, Iterable, DefaultDict
from asyncio import Task
from functools import partial
from logging import Logger
from enum import Enum
from contextvars import ContextVar

from ..core import StateIdentifier, CallbacksArg, CallbackList
from .nesting import StateTree

_LOGGER: Logger

class AsyncState(State):
    async def enter(self, event_data: AsyncEventData) -> None: ...
    async def exit(self, event_data: AsyncEventData) -> None: ...

class NestedAsyncState(NestedState, AsyncState):
    _scope: Any
    async def scoped_enter(self, event_data: AsyncEventData, scope: Optional[List[str]] = ...) -> None: ...
    async def scoped_exit(self, event_data: AsyncEventData, scope: Optional[List[str]] = ...) -> None: ...

class AsyncCondition(Condition):
    async def check(self, event_data: AsyncEventData) -> bool: ...

class AsyncTransition(Transition):
    condition_cls: Type[AsyncCondition]
    async def _eval_conditions(self, event_data: AsyncEventData) -> bool: ...
    async def execute(self, event_data: AsyncEventData) -> bool: ...
    async def _change_state(self, event_data: AsyncEventData) -> None: ...

class NestedAsyncTransition(AsyncTransition, NestedTransition):
    async def _change_state(self, event_data: AsyncEventData) -> None: ...

class AsyncEventData(EventData):
    machine: AsyncMachine
    transition: AsyncTransition
    source_name: Optional[str]
    source_path: Optional[List[str]]

class AsyncEvent(Event):
    machine: AsyncMachine
    transitions: DefaultDict[str, List[AsyncTransition]]

    async def trigger(self, model: object, *args, **kwargs) -> bool: ...
    async def _trigger(self, model: object, *args, **kwargs) -> bool: ...
    async def _process(self, event_data: AsyncEventData) -> bool: ...

class NestedAsyncEvent(NestedEvent):
    transitions: DefaultDict[str, List[NestedAsyncTransition]]

    async def trigger(self, event_data: AsyncEventData) -> bool: ...
    async def _process(self, event_data: AsyncEventData) -> bool: ...

class AsyncMachine(Machine):
    state_cls: Type[Union[AsyncState, NestedAsyncState]]
    transition_cls: Type[AsyncTransition]
    event_cls: Type[AsyncEvent]
    async_tasks: Dict[int, List[Task]]
    events: Dict[str, AsyncEvent]
    protected_tasks: List[Task]
    current_context: ContextVar
    _transition_queue_dict: Dict[int, Deque[Callable]]
    def __init__(self, *args, **kwargs) -> None: ...
    def add_model(self, model: Union[Union[Machine.self_literal, object], List[Union[Machine.self_literal, object]]],
                  initial: StateIdentifier = ...) -> None: ...
    async def dispatch(self, trigger: str, *args, **kwargs) -> bool: ...
    async def callbacks(self, funcs: Iterable[Union[str, Callable]], event_data: AsyncEventData) -> None: ...
    async def callback(self, func: Union[str, Callable], event_data: AsyncEventData) -> None: ...
    @staticmethod
    async def await_all(callables: List[Callable]) -> List: ...
    async def switch_model_context(self, model: object) -> None: ...
    def get_state(self, state: Union[str, Enum]) -> AsyncState: ...
    async def process_context(self, func: partial, model: object) -> bool: ...
    def remove_model(self, model: object) -> None: ...
    def _process(self, trigger: partial) -> bool: ...
    async def _process_async(self, trigger: partial, model: object) -> bool: ...


class HierarchicalAsyncMachine(HierarchicalMachine, AsyncMachine):
    state_cls: Type[NestedAsyncState]
    transition_cls: Type[NestedAsyncTransition]
    event_cls: Type[NestedAsyncEvent]
    async def trigger_event(self, _model: object, _trigger: str, *args, **kwargs): ...
    async def _trigger_event(self, event_data: AsyncEventData, trigger: str) -> bool: ...


class AsyncTimeout(AsyncState):
    dynamic_methods: List[str]
    timeout: float
    _on_timeout: CallbacksArg
    runner: Dict[int, Task]
    def __init__(self, *args, **kwargs) -> None: ...
    async def enter(self, event_data: AsyncEventData) -> None: ...
    async def exit(self, event_data: AsyncEventData) -> None: ...
    def create_timer(self, event_data: AsyncEventData): ...
    async def _process_timeout(self, event_data: AsyncEventData) -> None: ...
    @property
    def on_timeout(self) -> CallbackList: ...
    @on_timeout.setter
    def on_timeout(self, value: CallbacksArg) -> None: ...

class _DictionaryMock(dict):
    _value: Any
    def __init__(self, item) -> None: ...
    def __setitem__(self, key: Any, item: Any) -> None: ...
    def __getitem__(self, key: Any) -> Any: ...
    def __repr__(self) -> str: ...
