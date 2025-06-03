import logging
import json
from typing import Any, Dict

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a file handler
file_handler = logging.FileHandler('travel_agent.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class AiTravelAgentFunctionConfig(FunctionBaseConfig, name="ai_travel_agent"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    parameter: str = Field(default="default_value", description="Notional description for this parameter")


@register_function(config_type=AiTravelAgentFunctionConfig)
async def ai_travel_agent_function(
    config: AiTravelAgentFunctionConfig, builder: Builder
):
    logger.info("Starting ai_travel_agent_function")
    logger.debug(f"Configuration: {config.dict()}")

    # Implement your function logic here
    async def _response_fn(input_message: str) -> str:
        logger.info(f"Processing input message: {input_message}")
        
        try:
            # Process the input_message and generate output
            output_message = f"Hello from ai_travel_agent workflow! You said: {input_message}"
            logger.info(f"Generated output message: {output_message}")
            return output_message
        except Exception as e:
            logger.error(f"Error processing input message: {str(e)}", exc_info=True)
            raise

    try:
        logger.info("Yielding function info")
        yield FunctionInfo.create(single_fn=_response_fn)
    except GeneratorExit:
        logger.warning("Function exited early!")
    except Exception as e:
        logger.error(f"Unexpected error in ai_travel_agent_function: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Cleaning up ai_travel_agent workflow.")