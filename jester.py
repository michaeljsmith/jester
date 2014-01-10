import unittest

def beginObject():
  #print('beginning object')
  pass

def endObject():
  #print('ending object')
  pass

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

class Types(object):
  nextId = 100

  @staticmethod
  def newType(stem):
    id = Types.nextId
    Types.nextId += 1
    name = stem + str(id)
    return name

class Expected(object):
  def __init__(self, type_):
    self.type_ = type_

class Patterns(object):
  
  @staticmethod
  def unify(pattern, type_):
    if Patterns.isForm(pattern):
      return Patterns.unifyForm(pattern, type_)
    elif Patterns.isExpectation(pattern):
      return Patterns.unifyExpectation(pattern, type_)
    else:
      asdf

  @staticmethod
  def isForm(pattern):
    return type(pattern) == list

  @staticmethod
  def isExpectation(pattern):
    return type(pattern) == Expected

  @staticmethod
  def unifyExpectation(pattern, type_):
    if pattern.type_ == type_:
      return []
    else:
      return None

class TypeDefs(object):
  def __type(type_):
    return Types.newType(type_.__name__)

  @__type
  class app: pass

class App(object):
  def run(self):
    pass

class BuiltinDefs(object):

  dummyApp = TypedObject(TypeDefs.app, App())

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

class UnificationTests(unittest.TestCase):
  def testUnifySimpleTypeSucceeds(self):
    type_ = Types.newType('Foo')
    bindings = Patterns.unify(Expected(type_), type_)
    self.assertEquals(bindings, [])

  def testUnifySimpleTypeFails(self):
    expectedType = Types.newType('Foo')
    actualType = Types.newType('Bar')
    bindings = Patterns.unify(Expected(expectedType), actualType)
    self.assertEquals(bindings, None)

class EvaluationTests(unittest.TestCase):

  def setUp(self):
    pass

  def testEvaluateAndRunApp(self):

    with ObjectScope():
      app_ = evaluate(builtinEnv, app())
      if app_.type() != TypeDefs.app:
        asdf
      else:
        app_.object().run()

if __name__ == '__main__':
    unittest.main()

