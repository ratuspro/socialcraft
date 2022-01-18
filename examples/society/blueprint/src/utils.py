class Utils:
    @staticmethod
    def get_entities_in_range(entities, reference_position, range: float):
        close_entities = []
        for entity_key in entities:
            if reference_position.distanceTo(entities[entity_key].position) <= range:
                close_entities.append(entity_key)
        return close_entities

    @staticmethod
    def chat_if_close(message, emitter_position, bot):
        for entity_key in bot.entities:
            if (
                bot.entities[entity_key].name == "player"
                and bot.entities[entity_key].username == "ratuspro"
                and emitter_position.distanceTo(bot.entities[entity_key].position) <= 5
            ):
                print(message)
                bot.chat(message)
