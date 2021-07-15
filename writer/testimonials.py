class Testimonial:
        
    def __init__(self, text, name,job,id=1,img=''):
        self.text=text
        self.id=id
        self.name=name
        self.job=job
        self.img=img
        pass

    def __repr__(self):
        return self.text+' '+str(self.name)+self.job+self.img



testimonials=[
    # Testimonial(name='Jennifer Kirk',job='Freelancer',text="This AI is freaking incredible. Writing content used to take hours and I would be burnt out by the end of each day. I can spark creativity at any point in the day - whether I'm building out trainings, youtube videos, copywriting for social media, or creating books for lead generation. My only wish is that the website could write in more than just one brand voice from one account. Thank you!! for developing such a life saving tool"),
    Testimonial(name='Jason Bargeman',job='Serial Entreprenuer. Avid Reader & Writer.',text="Used TextBazaar out of curiosity and a love for AI as well as new tech on Product Hunt.. stayed because 'Woahh'. In the first 3 days I have created about 40,000 words worth content of newsletter emails, 20,000 words of articles/video scripts, and last weekend was able to write a small 13,000 word book that is now published. On top of the sheer volume, I am amazed at the quality."),
    Testimonial(name='Emily Andrew',job='Marketing Head',text="A 2 week copy project, finished in a day! If you suffer with 'getting the ball rolling' with copy - prepare to suffer no more. For two weeks the team was dragging their feet to rewrite our website and post content to our Instagram account. Using TextBazaar, we did it within a day with the content creation capabilities + tidbits of editing."),
    Testimonial(name='Steve W.',job='Freelancer',text="Loving this app. I am a pretty good copywriter, but this thing is gold! It will save me a ton of time coming up with fresh content. I give it some basic headlines and it emails me better content then the best freelancers I could hire on Fiverr and Upwork"),
    Testimonial(name='Kyla Weber',job='CMO',text="Keeping up with our content schedule with various mediums (i.e. ads, blogs, websites, social media, youtube, etc.) has been getting more and more difficult to write, which can easily burnout our writing team. TextBazaar, however, is an incredible tool that is sure to be a game changer and it's really changed content creation quality AND speed for the better for our business."),
]