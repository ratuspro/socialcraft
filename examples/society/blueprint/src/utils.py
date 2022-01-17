class Utils:
    @staticmethod
    def get_entities_in_range(entities, reference_position, range: float):
        close_entities = []
        for entity_key in entities:
            if reference_position.distanceTo(entities[entity_key].position) <= range:
                close_entities.append(entity_key)
        return close_entities
