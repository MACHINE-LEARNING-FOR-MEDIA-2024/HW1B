phrase = ("Glitch is something that extends beyond the most literal "
          "technological mechanics: it helps us to celebrate failure as a generative force...")

MARGIN = 40
words = []
drawnWords = []
wordCount = 0
nextUpdateMillis = 0
minTextSize = 20
maxTextSize = 30
cx = MARGIN
cy = MARGIN
spaceWidth = 0
lineHeight = 0

class FadingWord:
    def __init__(self, _word, _wordDelay):
        self.word = _word
        self.alpha = 255
        self.startTime = millis()
        self.letterDelay = _wordDelay / len(self.word)

        self.red = 0
        self.font = createFont( 'Roboto-Regular', 15 ) 
        self.size = minTextSize
        self.yOffset = 0
        self.fadeVel = -0.3

        if self.word.lower() == "glitch" or random(1) > 0.95:
            self.word = self.word.upper()
            self.red = 200
            self.font = createFont( 'Roboto-Italic', 15 ) 
            self.size = maxTextSize
            self.yOffset = -self.size / 6
            self.fadeVel = -0.01

        textFont(self.font)
        textSize(self.size)
        self.width = textWidth(self.word)

        # Set word positioning
        global cx, cy
        if cx + self.width > width - MARGIN:
            cx = MARGIN
            cy += lineHeight
            if cy > height - MARGIN:
                cy = MARGIN

        self.x = cx
        self.y = cy
        cx += self.width + spaceWidth

    def update(self):
        self.alpha += self.fadeVel

    def draw(self):
        elapsed = millis() - self.startTime
        lastLetter = min(int(elapsed / self.letterDelay), len(self.word))
        letters = self.word[:lastLetter]

        fill(self.red, 0, 0, self.alpha)  
        textFont(self.font)
        textSize(self.size)
        text(letters, self.x, self.y + self.yOffset)

# Setup function
def setup():
    global spaceWidth, lineHeight, words
    fullScreen()
    words = phrase.split(" ")
    textAlign(LEFT, TOP)
    textFont(createFont( 'Roboto-Regular', 15 ))  
    textSize(minTextSize)
    spaceWidth = textWidth(" ")
    lineHeight = 1.5 * minTextSize

# Check if the word is visible
def isVisible(fw):
    return fw.alpha > 0

# Main draw loop
def draw():
    global wordCount, nextUpdateMillis
    background(220)

    # Remove invisible words
    drawnWords[:] = [fw for fw in drawnWords if isVisible(fw)]
    
    # Update and draw words
    for fw in drawnWords:
        fw.update()
        fw.draw()
    
    # Add a new word if necessary
    if millis() > nextUpdateMillis:
        nextWordIndex = wordCount % len(words)
        nextWord = words[nextWordIndex]
        wordDelay = random(450, 600)
        drawnWords.append(FadingWord(nextWord, wordDelay))
        wordCount += 1
        nextUpdateMillis = millis() + 1.2 * wordDelay
