import asyncio
import traceback

class ReplMod:
    rank = 510
    help_dict = {'py_repl': 'repl, stolen from R. Danny'}

    def __init__(self, client, message):
        self.bot = client
        self.message = message

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    async def py_repl(self):
        msg = self.message

        repl_locals = {}
        repl_globals = {
            'bot': self.bot,
            'message': msg,
            'last': None
        }

        await self.bot.send_message(self.message.channel, 'Enter code to execute or evaluate. `exit()` or `quit` to exit.')
        while True:
            response = await self.bot.wait_for_message(author=msg.author, channel=msg.channel,
                                                       check=lambda m: m.content.startswith('`'))

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await self.bot.send_message(self.message.channel, 'Exiting.')
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await self.bot.send_message(self.message.channel, self.get_syntax_error(e))
                    continue

            repl_globals['message'] = response

            try:
                result = executor(code, repl_globals, repl_locals)
                if asyncio.iscoroutine(result):
                    result = await result
            except Exception as e:
                await self.bot.send_message(self.message.channel, '```py\n{}\n```'.format(traceback.format_exc()))
            else:
                if result is not None:
                    await self.bot.send_message(self.message.channel, '```py\n{}\n```'.format(result))
                    repl_globals['last'] = result
