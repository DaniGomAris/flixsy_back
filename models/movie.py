class Movie:
    def __init__(self, title, genre, year, rating, description, image_url):
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating
        self.description = description
        self.image_url = image_url

    def to_dict(self):
        return self.__dict__
