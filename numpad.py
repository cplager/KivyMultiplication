import kivy
import re
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.button     import Button
from kivy.uix.label      import Label
from kivy.clock          import Clock
from kivy.app            import App
from random              import randrange
from datetime            import datetime

digitRE = re.compile(r'^\d$')

class MultiplicationPracticeApp(App):

    def __init__(self):
        super(MultiplicationPracticeApp, self).__init__()
        self.currentQuestion = ''
        self.qNum            = 0
        self.numTot          = 10
        self.numbers         = range(3,10)
        self.numCorrect      = 0
        self.current         = '0'
        self.maxNumDigits    = 2
        self.askingQuestion  = False

        
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
        
        
    def summary(self):
        self.currentQuestion = ''
        total = (datetime.now() - self.startTime).total_seconds() / self.qNum
        pcnt  = 100. * self.numCorrect / self.qNum
        self.question.text = "Finished: %d / %d (%.1f%%) avg %.1f seconds each" \
              % (self.numCorrect, self.qNum, pcnt, total)
        self.numCorrect = 0
        self.qNum       = 0
        
        
    def nextQuestion(self, other=None):
        self.current = '0'
        self.updateDisplay()
        if self.qNum == self.numTot:
            # summary
            self.summary()
            return
        first  = self.numbers[randrange(len(self.numbers))]
        second = randrange(2, 10)
        if randrange(2):
            first, second = second, first
        self.currentQuestion = '%d x %d' %(first, second)
        self.currentAnswer   = first * second
        self.qNum           += 1
        self.question.text   = '%3d / %d: %s' % (self.qNum, self.numTot, self.currentQuestion)
        self.askingQuestion  = True
        
        
    def number(self, instance):
        if not self.askingQuestion:
            return
        value = instance.text
        if value == 'Done':
            value = int(self.current)
            self.fullEntry(value)
            self.askingQuestion = False
            return
        elif digitRE.search(value):
            if len(self.current) > self.maxNumDigits:
                # don't bother
                return
            if value == '0' and self.current == '0':
                # it's a zero and we hit zero. don't bother
                return
            if self.current == '0':
                self.current = value
            else:
                self.current += value
        elif value == "<":
            # removing digits
            if self.current == "0":
                # nothing to do
                return
            if len(self.current) == 1:
                # it's a single non-zero digit
                self.current = '0'
            else:
                self.current = self.current[:-1]
        self.updateDisplay()


    def updateDisplay(self):
        current = self.current
        if current == '0':
            current = ''
        self.answer.text = current


    def fullEntry(self, value):
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
        self.question.text = text
        Clock.schedule_once(self.nextQuestion, 5)

        
    def build(self):
        # Overall layout
        layout = GridLayout(cols=1)
        # Control row
        row1   =  BoxLayout(orientation='horizontal')
        layout.add_widget(row1)
        row1.add_widget(Button(text="start", on_press=self.control))
        row1.add_widget(Button(text="end"  , on_press=self.control))
        row1.add_widget(Button(text="exit" , on_press=self.control))
        # text
        row2   =  BoxLayout(orientation='horizontal')
        layout.add_widget(row2)
        # Question label
        self.question = Label(text="",  markup=True)
        row2.add_widget(self.question)
        # answer label
        self.answer = Label(text="", markup=True)
        row2.add_widget(self.answer)
        # number rows
        lines = []
        for outer in range(3):
            lines.append(['%s' % (3 * outer + x + 1) for x in range(3)])
        lines.reverse()
        lines.append(["<","0","Done"])
        for line in lines:
            row = BoxLayout(orientation='horizontal') 
            layout.add_widget(row)
            for value in line:
                num = Button(text=value, on_press=self.number,  background_color=[1,0,0,1])
                row.add_widget(num)
        return layout

MultiplicationPracticeApp().run()