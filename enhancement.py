from data_mapping import DataMappingCollection


class EnhancementFactory:
    @staticmethod
    def create(enhancement):

        craft_type = enhancement['craft_type']

        if craft_type % 2 != 0:
            return EnchantGem(enhancement)
        else:
            return GrindStone(enhancement)


class Enhancement:
    def __init__(self, enhancement):
        self.type_id = str(enhancement['craft_type_id'])
        self.id = str(enhancement['craft_item_id'])
        self.type = None

        self.is_ancient = None
        self.rune_set = None
        self.stat = None
        self.grade = None
        self.grade_int = 0
        self.min_value = 0
        self.max_value = 0

        self.set_is_ancient()
        self.set_enhancement_sets()
        self.set_enhancement_stat()
        self.set_enhancement_grade()

    def set_is_ancient(self):
        self.is_ancient = int(self.type_id[-2:]) >= 10

    def set_enhancement_sets(self):

        set_id = int(self.type_id[0:-4])
        _set = DataMappingCollection.get_rune_set(set_id)
        _ancient = "Ancient-" if self.is_ancient else ""

        self.rune_set = "{}{}".format(_ancient, _set)

    def set_enhancement_stat(self):
        type_id = int(self.type_id[-4:-2])
        self.stat = DataMappingCollection.get_rune_stat_type(type_id)

    def set_enhancement_grade(self):
        self.grade_int = int(self.type_id[-1])
        self.grade = DataMappingCollection.get_rune_grade(self.grade_int)

    def __eq__(self, other):
        return self.type_id == other.type_id

    def get_rune_set(self):
        """ getter used as 'polymorphsm' with rune object """

        return self.rune_set

    def show_detail(self):
        # Example: Enchant Legend Violent Spd (9 - 15)
        print("{} {} {} {} ({} - {})\n".format(self.type, self.grade, self.rune_set, self.stat, self.min_value, self.max_value))


class EnchantGem(Enhancement):
    def __init__(self, enhancement):
        super().__init__(enhancement)
        self.type = "Enchant"
        self.set_values()

    def set_values(self):
        self.min_value = DataMappingCollection.get_enchantgem_value_min(self.stat, self.grade)
        self.max_value = DataMappingCollection.get_enchantgem_value_max(self.stat, self.grade)


class GrindStone(Enhancement):
    def __init__(self, enhancement):
        super().__init__(enhancement)
        self.type = "Grind"
        self.set_values()

    def set_values(self):
        self.min_value = DataMappingCollection.get_grindstone_value_min(self.stat, self.grade)
        self.max_value = DataMappingCollection.get_grindstone_value_max(self.stat, self.grade)
