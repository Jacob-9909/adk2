# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sequential graph workflow: random city → lookup time (code) → LLM report → done.

ADK 2.0 `Workflow` + `google.adk.Agent` entry points. Run: `adk web agents` from repo root.
"""

from __future__ import annotations

import os

from google.adk import Agent
from google.adk import Event
from google.adk import Workflow
from pydantic import BaseModel

_MODEL = os.environ.get("MODEL", "gemini-2.5-flash")

city_generator_agent = Agent(
    name="city_generator_agent",
    model=_MODEL,
    instruction="""Return the name of a random city.
      Return only the name, nothing else.""",
    output_schema=str,
)


class CityTime(BaseModel):
    time_info: str
    city: str


def lookup_time_function(node_input: str):
    """Return simulated local time for the given city name."""
    return CityTime(time_info="10:10 AM", city=node_input)


city_report_agent = Agent(
    name="city_report_agent",
    model=_MODEL,
    input_schema=CityTime,
    instruction="""Output following line:
    It is {CityTime.time_info} in {CityTime.city} right now.""",
    output_schema=str,
)


def completed_message_function(node_input: str):
    return Event(message=f"{node_input}\n WORKFLOW COMPLETED.")


root_agent = Workflow(
    name="city_workflow",
    edges=[
        (
            "START",
            city_generator_agent,
            lookup_time_function,
            city_report_agent,
            completed_message_function,
        )
    ],
)
