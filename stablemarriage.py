
class Suitor(object):
   def __init__(self, id, prefList):
      self.prefList = prefList
      self.rejections = 0 # num rejections is also the index of the next option
      self.id = id

   def preference(self):
      return self.prefList[self.rejections]

   def __repr__(self):
      return repr(self.id)


class Suited(object):
   def __init__(self, id, prefList, capacity=1):
      self.prefList = prefList
      self.capacity = capacity
      self.held = set()
      self.id = id

   def reject(self):
      # trim the self.held set down to its capacity, returning the list of rejected suitors.

      if len(self.held) < self.capacity:
         return set()
      else:
         sortedSuitors = sorted(list(self.held), key=lambda suitor: self.prefList.index(suitor.id))
         self.held = set(sortedSuitors[:self.capacity])

         return set(sortedSuitors[self.capacity:])

   def __repr__(self):
      return repr(self.id)


# stableMarriage: [Suitor], [Suited] -> {Suited -> [Suitor]}
# construct a stable (polygamous) marriage between suitors and suiteds
def stableMarriage(suitors, suiteds):
   unassigned = set(suitors)

   while len(unassigned) > 0:
      for suitor in unassigned:
         suiteds[suitor.preference()].held.add(suitor)
      unassigned = set()

      for suited in suiteds:
         unassigned |= suited.reject()

      for suitor in unassigned:
         suitor.rejections += 1

   return dict([(suited, sorted(suited.held, key=lambda x: x.id)) for suited in suiteds])


# verifyStable: [Suitor], [Suited], {Suited -> [Suitor]} -> bool
# check that the assignment of suitors to suited is a stable marriage
def verifyStable(suitors, suiteds, marriage):
   import itertools

   precedes = lambda L, item1, item2: L.index(item1) < L.index(item2)
   partner = lambda suitor: filter(lambda s: suitor in marriage[s], suiteds)[0] # unique

   def suitorPrefers(suitor, suited):
      return precedes(suitor.prefList, suited.id, partner(suitor).id)

   def suitedPrefers(suited, suitor):
      return any(map(lambda x: precedes(suited.prefList, suitor.id, x.id), marriage[suited]))

   for (suitor, suited) in itertools.product(suitors, suiteds):
      if suitor not in marriage[suited] and suitorPrefers(suitor, suited) and suitedPrefers(suited, suitor):
         return False

   return True


if __name__ == "__main__":
   from unittest import test

   suitors = [Suitor(0, [0,1]), Suitor(1, [1,0])]
   suiteds = [Suited(0, [0,1], 1), Suited(1, [1,0], 1)]
   marriage = stableMarriage(suitors, suiteds)
   test({suiteds[0]:[suitors[0]], suiteds[1]:[suitors[1]]}, marriage)
   test(True, verifyStable(suitors, suiteds, marriage))

   suitors = [Suitor(0, [0]), Suitor(1, [0]), Suitor(2, [0]), Suitor(3, [0])]
   suiteds = [Suited(0, [0,1,2,3], 4)]
   marriage = stableMarriage(suitors, suiteds)
   test({suiteds[0]: suitors}, marriage)
   test(True, verifyStable(suitors, suiteds, marriage))

   suitors = [Suitor(0, [0,1]), Suitor(1, [0,1]), Suitor(2, [0,1]), Suitor(3, [0,1])]
   suiteds = [Suited(0, [0,1,2,3], 2), Suited(1, [3,2,1,0], 2)]
   marriage = stableMarriage(suitors, suiteds)
   test({suiteds[0]: suitors[:2], suiteds[1]: suitors[2:]}, marriage)
   test(True, verifyStable(suitors, suiteds, marriage))

   # more tests
