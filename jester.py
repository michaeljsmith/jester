def beginObject():
  print('beginning object')

def endObject():
  print('ending object')

class ObjectScope(object):
  def __enter__(self):
    beginObject()

  def __exit__(self, exc_type, exc_value, traceback):
    endObject()

def evaluate(env, expr):
  if isForm(expr):
    return evaluateForm(env, expr)
  else:
    return asdf

def main():
  with ObjectScope():
    app_ = evaluate(app)
    app_.run()

if __name__ == '__main__':
  main()
