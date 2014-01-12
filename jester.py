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
  def newFinite(stem):
    id = Types.nextId
    Types.nextId += 1
    name = stem + str(id)
    return name

  @staticmethod
  def match(expected, actual):
    if Types.isForm(expected):
      return Types.matchForm(expected, actual)
    elif Types.isExpectation(expected):
      return Types.matchExpectation(expected, actual)
    elif Types.isReference(expected):
      return Types.matchReference(expected, actual)
    else:
      asdf

  @staticmethod
  def isForm(expected):
    return type(expected) == list

  @staticmethod
  def isExpectation(expected):
    return type(expected) == Expected

  @staticmethod
  def isReference(expected):
    return type(expected) == Reference

  @staticmethod
  def matchExpectation(expected, actual):
    if expected.actual == actual:
      return []
    else:
      return None

  @staticmethod
  def matchReference(expected, actual):
    return [expected.name, actual]

class Expected(object):
  def __init__(self, type_):
    self.type_ = type_

class Universal(object):
  def __init__(self, vars_, body):
    self.vars = vars_
    self.body = body

class Reference(object):
  def __init__(self, name):
    self.name = name

class TypeDefs(object):
  def __type(type_):
    return Types.newFinite(type_.__name__)

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
    type_ = Types.newFinite('Foo')
    bindings = Types.match(Expected(type_), type_)
    self.assertEquals(bindings, [])

  def testUnifySimpleTypeFails(self):
    expectedType = Types.newFinite('Foo')
    actualType = Types.newFinite('Bar')
    bindings = Types.match(Expected(expectedType), actualType)
    self.assertEquals(bindings, None)

  def testUnifyVarSucceeds(self):
    type_ = Types.newFinite('Foo')
    bindings = Types.match(Universal(['T'], Reference(['T'])), type_)
    self.assertEquals(bindings, [('T', type_)])

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

