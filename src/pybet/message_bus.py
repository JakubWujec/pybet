from src.pybet import commands, events, services, unit_of_work
from typing import Dict, List, Type, Callable, Union

Message = Union[events.Event, commands.Command]

def handle(message: Message, uow: unit_of_work.UnitOfWork):
    if isinstance(message, commands.Command):
        handle_command(message, uow)
        
    if isinstance(message, events.Event):
        handle_event(message, uow)
    

def handle_event(event: events.Event, uow: unit_of_work.UnitOfWork):
    for handler in EVENT_HANDLERS[type(event)]:
        handler(event, uow) 

def handle_command(command: commands.Command, uow: unit_of_work.UnitOfWork):
    handler = COMMAND_HANDLERS[type(command)]
    handler(command, uow)

COMMAND_HANDLERS: Dict[Type[events.Event], Callable] = {
    commands.UpdateMatchScoreCommand: services.update_match_score,
    commands.MakeBetCommand: services.make_bet
}

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.MatchScoreUpdated: [services.update_bet_points_for_match]
}



