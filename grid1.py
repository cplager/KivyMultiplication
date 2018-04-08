import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.button     import Button
from kivy.uix.label      import Label
from kivy.app            import App
from random              import randrange
from datetime            import datetime


class MultiplicationPracticeApp(App):

    def __init__(self):
        super(MultiplicationPracticeApp, self).__init__()
        self.currentQuestion = ''
        self.qNum = 0
        self.numTot = 10
        self.numbers = range(3,10)
        self.numCorrect = 0

        
    def control(self, instance):
        if instance.text == "exit":
            App.get_running_app().stop()
            return
        if instance.text == "start":
            self.qNum = 0
            self.startTime = datetime.now()
            self.nextQuestion()
            return
        if instance.text == "end":
            self.summary()
            return 
        print instance.text, "pressed"
        
        
    def summary(self):
        self.currentQuestion = ''
        total = (datetime.now() - self.startTime).total_seconds() / self.qNum
        pcnt = 100. * self.numCorrect / self.qNum
        self.question.text = "Finished: %d / %d (%.1f%%) avg %.1f seconds each" \
              % (self.numCorrect, self.qNum, pcnt, total)
        self.numCorrect = 0
        self.qNum = 0
        
        
    def nextQuestion(self):
        if self.qNum == self.numTot:
            # summary
            self.summary()
            return
        first  = self.numbers[randrange(len(self.numbers))]
        second = randrange(2, 10)
        if randrange(2):
            first, second = second, first
        self.currentQuestion = '%d x %d' %(first, second)
        self.currentAnswer = first * second
        self.qNum += 1
        self.question.text = '%3d / %d: %s' % (self.qNum, self.numTot, self.currentQuestion)
        
        
    def number(self, instance):
        value = int(instance.text)
        if not self.currentQuestion:
            return
        if value == self.currentAnswer:
            # correct()
            text = '[color=00ff00]Correct! %s = %d[/color]' % \
                    (self.currentQuestion, value)
            self.numCorrect += 1
        else:
            # wrong
            text = '[color=ff0000]Wrong! %s = %d, not %d[/color]' % \
                    (self.currentQuestion, self.currentAnswer, value)
        self.answer.text = text
        self.nextQuestion()

        
    def build(self):
        # Overall layout
        layout = GridLayout(cols=1, row_force_default=True, row_default_height=40)
        # Control row
        row1   =  BoxLayout(orientation='horizontal')
        layout.add_widget(row1)

        row1.add_widget(Button(text="start", on_press=self.control))
        row1.add_widget(Button(text="end"  , on_press=self.control))
        row1.add_widget(Button(text="exit" , on_press=self.control))
        # Question label
        self.question = Label(text="Question", font_size='20sp')
        layout.add_widget(self.question)
        # number rows
        for loop in range(1,101):
            if loop % 10 == 1:
                row = BoxLayout(orientation='horizontal') 
                layout.add_widget(row)
            num = Button(text='%d' % loop, on_press=self.number,  background_color=[1,0,0,1])
            row.add_widget(num)
        # answer label
        self.answer = Label(text="answer", font_size='20sp', markup=True)
        layout.add_widget(self.answer)
        return layout

MultiplicationPracticeApp().run()