#
# Copyright (c) 2022 ZettaScale Technology
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: EPL-2.0 OR Apache-2.0
#
# Contributors:
#   ZettaScale Zenoh Team, <zenoh@zettascale.tech>
#

from zenoh_flow.interfaces import Source
from zenoh_flow import Outputs
from zenoh_flow.types import Context
from typing import Any, Dict
import asyncio


class MySource(Source):
    def __init__(
        self,
        context: Context,
        configuration: Dict[str, Any],
        outputs: Outputs,
    ):
        configuration = {} if configuration is None else configuration
        self.value = int(configuration.get("value", 0))
        # self.output = outputs.("Value", None)
        self.output = outputs.take(
            "Value", int, lambda x: x.to_bytes((x.bit_length() + 7) // 8, "big")
        )

    def finalize(self) -> None:
        return None

    def produce_data(self):
        self.value += 1
        print(f"Sending {self.value}")
        return self.value

    async def iteration(self) -> None:
        await asyncio.sleep(0.5)
        await self.output.send(self.produce_data())
        return None


def register():
    return MySource
