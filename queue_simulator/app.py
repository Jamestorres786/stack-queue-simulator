from flask import Flask, render_template, request

app = Flask(__name__)

class Queue:
    def __init__(self):
        self.items = []
        self.removed_items = []
        self.front_value = None

    def enqueue(self, value):
        if value.strip() != "":
            self.items.insert(0, value.strip())

    def dequeue(self):
        if not self.is_empty():
            val = self.items.pop()
            self.removed_items.append(val)
            return val
        return None

    def front(self):
        if not self.is_empty():
            self.front_value = self.items[-1]
            return self.items[-1]
        self.front_value = None
        return None

    def clear(self):
        self.items = []
        self.removed_items = []
        self.front_value = None

    def is_empty(self):
        return len(self.items) == 0

queue = Queue()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        action = request.form.get('action')
        value = request.form.get('value', '')

        if action == 'enqueue':
            if value.strip() == "":
                message = "⚠️ Ilagay ang halaga bago mag-enqueue."
            else:
                queue.enqueue(value)
        elif action == 'dequeue':
            if queue.is_empty():
                message = "⚠️ Walang laman ang pila — hindi makapag-dequeue."
            else:
                queue.dequeue()
        elif action == 'front':
            if queue.is_empty():
                message = "⚠️ Walang laman ang pila — walang nasa unahan."
            else:
                queue.front()
        elif action == 'clear':
            queue.clear()

    return render_template('index.html', items=queue.items, removed_items=queue.removed_items, front_value=queue.front_value, message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
