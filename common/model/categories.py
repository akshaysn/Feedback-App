class CategoryDetail:
	def __init__(self, code, displayName, show_time=False):
		self.code = code
		self.displayName = displayName
		self.show_time = show_time

class Category:
	TALK = CategoryDetail('talk', 'Talk', True)
	EVENT = CategoryDetail('event', 'Event Related')
	
	CONF = CategoryDetail('conf', 'Conference')

	BLITZ = CategoryDetail('blitz', 'Blitz (6 mins)')
	RAPID = CategoryDetail('rapid', 'Rapid (30 mins)', True)
	CLASSIC = CategoryDetail('classic', 'Classic (60 mins)', True)
	XCONF = CategoryDetail('xconf', 'XConf')

category_factory =	{
    "TALK":Category.TALK,
    "EVENT":Category.EVENT,
    "CONF":Category.CONF,
    "BLITZ":Category.BLITZ,
    "RAPID":Category.RAPID,
    "CLASSIC":Category.CLASSIC,
    "XCONF":Category.XCONF
}
