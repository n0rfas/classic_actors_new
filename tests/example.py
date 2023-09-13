from classic.actors import actor, SuperVisor, S

s = S()


@actor
class Actor:

    @actor.method
    def s1(self, a, b):
        return a + b


supervisor = SuperVisor()

na1 = Actor()

supervisor.add(na1)

p1 = na1.s1(1, 2)
print(1)
supervisor.run()
print(2)
print('p1 = ', p1.get())
