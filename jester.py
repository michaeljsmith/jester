def beginObject():
  print('beginning object')

def endObject():
  print('ending object')

class ObjectScope(object):
  def __enter__(self):
    beginObject()

  def __exit__(self, exc_type, exc_value, traceback):
    endObject()

class Bindings(object):

  @staticmethod
  def lookup(bindings, sym):
    if not bindings:
      raise Exception('Symbol ' + sym + ' undefined.')
    elif bindings[0] == sym:
      return bindings[1]
    else:
      return lookup(bindings[2], sym)

class Environment(object):
  # TODO: Replace with immutable tree-based implementation.

  def __init__(self, bindings):
    self.bindings_ = bindings

  def lookup(self, sym):
    return Bindings.lookup(self.bindings_, sym)

class BuiltinDefs(object):

  dummyApp = TypedObject(Types.app, App())

builtinEnv = Environment([])

def isSymbol(expr):
  return type(expr) == str

def evaluate(env, expr):
  if isSymbol(expr):
    return evaluateSymbol(env, expr)
  elif isForm(expr):
    return evaluateForm(env, expr)

def evaluateSymbol(env, expr):
  return env.lookup(expr)

class Edsl(object):
  dummyApp = 'dummyApp'

def app():
  e = Edsl
  return e.dummyApp

def main():
  with ObjectScope():
    app_ = evaluate(builtinEnv, app())
    app_.run()

if __name__ == '__main__':
  main()
