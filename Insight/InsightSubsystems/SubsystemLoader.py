from InsightUtilities import InsightSingleton
import discord_bot
import service
import InsightLogger


class SubsystemLoader(metaclass=InsightSingleton):
    def __init__(self, discord_client):
        self.lg = InsightLogger.InsightLogger.get_logger('Subsystem.Loader', 'InsightUtilities.log', child=True)
        self.client: discord_bot.Discord_Insight_Client = discord_client
        self.service: service.ServiceModule = self.client.service
        self.insight_ready_event = self.client.insight_ready_event
        self.loop = self.client.loop
        self.subsystems = []

    async def start_tasks(self):
        self.lg.info("Waiting for ready signal.")
        await self.insight_ready_event.wait()
        self.lg.info("Received ready signal... starting subsystem tasks.")
        for s in self.subsystems:
            self.loop.create_task(s.start_subsystem())

    async def stop_tasks(self):
        self.lg.info("Received shutdown signal... stopping subsystem tasks.")
        for s in self.subsystems:
            await s.stop_subsystem()