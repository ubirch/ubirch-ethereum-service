# coding: utf-8
#
# @author Victor Patrin
#
# Copyright (c) 2018 ubirch GmbH.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from libtest import *
from kafka import *

args = set_arguments("ethereum")
port = args.port

queue2 = KafkaConsumer('queue2', bootstrap_servers=port, value_deserializer=lambda m: json.loads(m.decode('ascii')))


for msg in queue2:
    print(json.dumps(msg.value))