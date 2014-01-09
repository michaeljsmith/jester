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

  @staticmethod
  def bindingsFromModule(mod):
    # TODO: Do in more functional way.
    bindings = []
    for k, v in ((k, v) for k, v in vars(mod).items() if not k.startswith('__')):
      bindings = k, v, bindings

    return bindings

class Environment(object):
  # TODO: Replace with immutable tree-based implementation.

  def __init__(self, bindings):
    self.bindings_ = bindings

  def lookup(self, sym):
    return Bindings.lookup(self.bindings_, sym)

  @staticmethod
  def fromModule(mod):
    return Environment(Bindings.bindingsFromModule(mod))

class TypedObject(object):
  def __init__(self, type_, obj_):
    self.type_ = type_
    self.obj_ = obj_

  def type(self):
    return self.type_

  def object(self):
    return self.obj_

class Type(object):
  def __init__(self, name):
    self.name = name

class Types(object):
  def __type(type_):
    return Type(type_.__name__)

  @__type
  class app: pass

class App(object):
  def run(self):
    print('running app')

class BuiltinDefs(object):

  dummyApp = TypedObject(Types.app, App())

builtinEnv = Environment.fromModule(BuiltinDefs)

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
    if app_.type() != Types.app:
      asdf
    else:
      app_.object().run()

if __name__ == '__main__':
  main()
