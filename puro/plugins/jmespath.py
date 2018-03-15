"""
JMESPath expressions as Puro actions

http://jmespath.org/
https://github.com/jmespath/jmespath.py

Notes:
- doesn't really care about being JSON, input/output is Python
  and can contain non-serializable items
- a variant of this could also be used as a selector
"""
import jmespath

from . import Action


class JMESPath(Action):
    plugin_name = "jmespath"

    def __init__(self, name, *, expression):
        super().__init__(name)
        self.expression = jmespath.compile(expression)

    async def __call__(self, task):
        task.value = self.expression.search(task.value)
