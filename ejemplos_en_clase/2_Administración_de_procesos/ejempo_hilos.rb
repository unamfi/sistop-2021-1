# coding: utf-8
class EjemploHilos
  def initialize
    @x=0
  end

  def f1
    print '+'
    @x += 3
  end

  def f2
    print '*'
    @x *= 2
  end

  def run
    t1 = Thread.new {f1}
    t2 = Thread.new {f2}
    print '%d '%@x
  end
end

puts "Ejecución 1:"
e = EjemploHilos.new
10.times {e.run}

puts ''
puts "Ejecución 2:"
e = EjemploHilos.new
10.times {e.run}

puts ''
