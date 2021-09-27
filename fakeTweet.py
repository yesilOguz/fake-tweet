from PIL import Image, ImageFont, ImageDraw
import random
from io import BytesIO
import textwrap
import datetime

class fakeTweet:
    def __init__(self, text:str, imPath:str, name:str, username:str=None, isVerified:bool=False):
        self.text = text
        self.im = Image.open(imPath)
        self.name = name
        self.username = username
        self.isVerified = isVerified

        tweetFeatures = ['Retweet', 'Quote Tweets', 'Likes']
        self.withNumbers = dict()
        
        for feature in tweetFeatures:
            rand = str(round(random.uniform(1.0, 10.9), 1))

            self.withNumbers[rand] = feature



    def GetDate(self):
        def Date(now):
            year = str(now.strftime('%Y'))
            day = str(now.strftime('%d'))
            month = str(now.strftime('%b'))

            datestr = "{} {}, {}".format(month, day, year)

            return datestr

        def Time(now):
            hour = str(now.strftime('%I'))
            minute = str(now.strftime('%M'))
            period = str(now.strftime('%p'))
            
            timestr = "{}:{} {}".format(hour, minute, period)
            
            return timestr

        x = datetime.datetime.now()

        return "{} · {} · Twitter for iPhone".format(Time(x), Date(x))
    

    def mask(self, image, bg):
        size = 50, 50
        
        resim = Image.open(image)
        back = Image.open(bg)

        resim.thumbnail(size, Image.ANTIALIAS)

        bigsize = (resim.size[0] * 3, resim.size[1] * 3)

        mask_im = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0) + bigsize, fill=255)

        mask = mask_im.resize(resim.size, Image.ANTIALIAS)

        back_im = back.copy()
        back_im.paste(resim, (5, 8), mask)

        bytePhoto = BytesIO()
        back_im.save(bytePhoto, "PNG")
        bytePhoto.seek(0)

        return bytePhoto
    

    def CreateTweet(self):
        ####    Fonts    ####
        fontPath = 'resource/arial.otf'
        mainFont = ImageFont.truetype(fontPath, 20)
        thinFont = ImageFont.truetype(fontPath, 17)
        featureFont = ImageFont.truetype(fontPath, 16)
        UsernameandDateFont = ImageFont.truetype(fontPath, 14)
        ####    Fonts    ####

        ####    colors    ####
        gray = (90,89,90)
        likeWhite = (250,250,250)
        white = (255,255,255)
        ####    colors    ####
        
        wrapper = textwrap.TextWrapper(width=50)
        wordList = wrapper.wrap(text=self.text)

        y = 170
        
        for word in wordList:
            font_size = mainFont.getsize(text=word)

            y+=font_size[1]
            
        bg = Image.new('RGB', (600, y), (0,0,0))
        draw = ImageDraw.Draw(bg)

        w, h = bg.size
        
        x,y = 11,70
        for write in wordList:
            draw.text((x,y), write, likeWhite, font=mainFont)
            y += 25

        date = self.GetDate()
        
        draw.text((14, (h - 68)), date, gray, font=UsernameandDateFont)
        draw.text((12, (h - 64)), "_"*80, gray, font=thinFont)
        draw.text((12, (h - 28)), "_"*80, gray, font=thinFont)
        draw.text((560, 13), '·'*3, gray, font=mainFont)
        
        i = 0
        x = 12
        for key, value in self.withNumbers.items():
            key = key+'K '
            draw.text((x, (h - 36)), key , likeWhite, font=featureFont)
            x += (featureFont.getsize(text=key))[0]
            
            draw.text((x, (h - 36)), value, gray, font=featureFont)
            x += (featureFont.getsize(text=value))[0] + 10
            
            i += 1

        bytePhoto = BytesIO()
        bg.save(bytePhoto, "PNG")
        bytePhoto.seek(0)        

        pp = BytesIO()
        self.im.save(pp, 'PNG')

        maskedPP = self.mask(pp, bytePhoto)

        tweet = Image.open(maskedPP)
        draw = ImageDraw.Draw(tweet)        

        verified = Image.open("resource/verified_twitter.png")
        size = 23, 23
        verified.thumbnail(size, Image.ANTIALIAS)

        if self.username is not None:
            draw.text((60, 13), self.name, white, font=featureFont)
            draw.text((60, 32), '@'+self.username, gray, font=UsernameandDateFont)

            if self.isVerified:
                tweet.paste(verified, ((featureFont.getsize(text=self.name))[0]+60, 11))
        else:
            draw.text((60, 20), self.name, white, font=featureFont)

            if self.isVerified:
                tweet.paste(verified, ((featureFont.getsize(text=self.name))[0]+60, 19))
        ByteTweet = BytesIO()
        tweet.save(ByteTweet, 'PNG')

        return ByteTweet
        
fake = fakeTweet(text='Hello Twitter', imPath='resource/joeBiden.jpg', name='President Biden', username='POTUS', isVerified=True)
fake.CreateTweet()
