class VoiceMod:

    rank = 0
    help_dict = {'py_soge': 'SogePlayz', 'py_stfu': 'ey thas pretty nice'}

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def vjoin(self):

        voice = self.client.voice_client_in(self.message.server)
        if voice is None:
            voice = await self.client.join_voice_channel(self.message.author.voice_channel)
            return voice
        return voice

    async def py_soge(self):
        voice = await self.vjoin()
        player = voice.create_ffmpeg_player('sounds/sogePlayz.mp3')
        player.start()

    async def py_stfu(self):
        voice = self.client.voice_client_in(self.message.server)
        if voice is None:
            return await self.client.send_message(self.message.channel, 'Not in a voice channel.')
        return await voice.disconnect()
