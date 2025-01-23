from pybet import commands, events, unit_of_work, handlers
from typing import Dict, List, Type, Callable, Union, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from pybet import unit_of_work
    
logger = logging.getLogger(__name__)

Message = Union[events.Event, commands.Command]

def handle(message: Message, uow: "unit_of_work.UnitOfWork"):
    queue = [message]
    while queue:
        _message = queue.pop()
        
        if isinstance(_message, commands.Command):
            handle_command(_message, queue, uow)
        elif isinstance(_message, events.Event):
            handle_event(_message, queue, uow)
        else:
            raise Exception(f'{message} was not an Event or Command')
           
    

def handle_event(event: events.Event, queue: List[Message], uow: "unit_of_work.UnitOfWork"):
    for handler in EVENT_HANDLERS[type(event)]:
        handler(event, uow)
        queue.extend(uow.collect_new_events()) 

def handle_command(command: commands.Command, queue: List[Message], uow: "unit_of_work.UnitOfWork"):
    logger.debug("handling command %s", command)
    try: 
        handler = COMMAND_HANDLERS[type(command)]
        handler(command, uow)
        queue.extend(uow.collect_new_events())
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise

COMMAND_HANDLERS: Dict[Type[events.Event], Callable] = {
    commands.CreateMatchCommand: handlers.create_match,
    commands.UpdateMatchScoreCommand: handlers.update_match_score,
    commands.MakeBetCommand: handlers.make_bet
}

EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.MatchScoreUpdated: [handlers.update_bet_points_for_match]
}



