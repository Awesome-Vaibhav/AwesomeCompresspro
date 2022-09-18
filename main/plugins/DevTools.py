#-----------------------------------------------------------------#
# THIS FILE IS UPLOADED TO AWESOME VAIBHAV VIDEO COMPRESSION BOT.
# ALL THE FUNCTIONS AND MODULES USED ARE FREE TO USE.
#-----------------------------------------------------------------#

from telethon import events

import asyncio

from io import BytesIO, StringIO
import traceback, json, sys
try:
    import black
except ModuleNotFoundError or ImportError:
    pass

from .. import Drone
from LOCAL.localisation import DEV

# HELPER FUNCTIONS

async def bash(cmd, run_code=0):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip() or None
    out = stdout.decode().strip() or "Success"
    return out, err

def _parse_eval(value=None):
    if not value:
        return value
    if hasattr(value, "stringify"):
        try:
            return value.stringify()
        except TypeError:
            pass
    elif isinstance(value, dict):
        try:
            return json.dumps(value, indent=1)
        except Exception:
            pass
    return str(value)

def _stringify(text=None, *args, **kwargs):
    if text:
        text = _parse_eval(text)
    return print(text, *args, **kwargs)

async def aexec(code, event):
    exec(
        (
            "async def __aexec(e, client): "
            + "\n p = print"
            + "\n message = event = e"
            + "\n reply = await event.get_reply_message()"
            + "\n chat = event.chat_id"
        )
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](event, event.client)

# MAIN FUNCTIONS (EXECUTION)

@Drone.on(events.MessageEdited(pattern='^(!|/)eval'))
@Drone.on(events.NewMessage(pattern='^(!|/)eval'))
async def _(event):
    sender = await event.get_sender()
    if f"https://t.me/{sender.username}" == DEV:
        cmd = str(event.text.split(" ", maxsplit=1)[1])
        edit = await event.reply("<code>Processing...</code>", parse_mode="HTML")
        if black:
            try:
                cmd = black.format_str(cmd, mode=black.Mode())
            except BaseException:
                pass
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()
        stdout, stderr, exc = None, None, None
        try:
            value = await aexec(cmd, event)
        except Exception:
            exc = traceback.format_exc()
        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = exc or stderr or stdout or _parse_eval(value) or "Success"
        final_output = ("__►__ **EVAL**\n```{}```\n\n__►__ **OUTPUT**: \n```{}```\n".format(cmd, evaluation))
        if exc:
            final_output+=f"__►__ **Error**: \n```{exc or stderr}```\n\n__Exception occurred while processing this code.__"
        if len(final_output)>4092:
            with open("Eval.txt", "w") as file:
                file.write(final_output)
            await event.client.send_file(event.chat_id, file='Eval.txt', reply_to = event.id)
        else:
            await edit.edit(final_output, parse_mode='md')

@Drone.on(events.MessageEdited(pattern='^(!|/)bash'))
@Drone.on(events.NewMessage(pattern='^(!|/)bash'))
async def _(event):
    sender = await event.get_sender()
    if f"https://t.me/{sender.username}" == DEV:
        cmd = str(event.text.split(" ", maxsplit=1)[1])
        edit = await event.reply("`Processing...`")
        result, error = await bash(cmd)
        final_output = f"<i>►</i> <b>Bash</b>\n<code>{cmd}</code>\n\n<i>►</i> <b>OUTPUT</b>: \n<code>{result}</code>"
        if not error in [None, ""]:
            final_output = f"<i>►</i> <b>Bash</b>\n<code>{cmd}</code>\n\n<i>►</i> <b>OUTPUT</b>: \n<code>{result}</code>\n\n<b>Error</b>: \n<code>{error}</code>"
        if len(final_output)>4092:
            with open("Bash.txt", "w") as file:
                file.write(final_output)
            await event.client.send_file(event.chat_id, file='Bash.txt', reply_to = event.id)
            await edit.delete()
        else:
            await edit.edit(final_output, parse_mode='html')
