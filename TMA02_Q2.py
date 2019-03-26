"""The Marathon ADT.

For TMA02 Question 2 of M269 17J.

@Author - Tom Harrison
@Version - 2.0 - March 2018
"""


class Marathon:

    # Creator
    # -------

    def __init__(self):
        """Set up this marathon without any runners."""
        self.reg_book = {}  # dictionary for {runner, time} pairs

        """finish list to keep track of runners that have
        finished the marathon"""
        self.finish_list = []  # store runners names in place order as they finish the race
        self.finish_list.append('NOT A RUNNER')  # dummy value to fill position 0 of the finish_list

    # Inspectors
    # ----------

    # These are called anytime.

    def registered(self, runner):
        """Return True if runner has registered, otherwise False."""
        if runner in self.reg_book:
            return True
        return False

    def finishers(self):
        """Return the number of starting who finished the race so far."""
        return len(self.finish_list) - 1

    def finished(self, runner):
        """Return True if runner has finished the race, otherwise False."""
        # first check that the runner is registered to the marathon
        if self.registered(runner):
            if self.reg_book[runner] != 0:  # if the runners time has been set (by .finished() method)
                return True
        return False

    # These inspectors are called after the race ends.

    def finishers_up_to(self, time):
        """Return how many runners finished in the given time or less.
        Assume the unit of time is seconds.
        """
        first = 1
        last = self.finishers()

        while first <= last:
            mid = (first + last) // 2

            # eval_time - the finishing time being evaluated on this iteration of the loop
            eval_time = self.reg_book.get(self.finish_list[mid])

            if eval_time == time:
                # correct time has been found
                # check to see if there are any duplicate times with a higher index in finish_list
                if self.reg_book.get(self.finish_list[mid + 1]) != time:
                    # there aren't any duplicates so return
                    return mid
                else:
                    dup_check = 2  # duplicate checker initialised to 2 (because mid+1 has already been checked)

                    while mid + dup_check <= self.finishers() and self.reg_book.get(
                            self.finish_list[mid + dup_check]) == time:
                        dup_check = dup_check + 1

                    # At this point mid+dupCheck has been found to be out of the lists bounds or has found
                    # a different (greater) time. So minus 1 to return only number of finishers
                    # within the time given."""
                    return mid + dup_check - 1

            elif eval_time < time:
                # correct time has not yet been found. Reduce search space
                first = mid + 1
            else:
                # correct time has not yet been found. Reduce search space
                last = mid - 1

        return last

    def place(self, runner):
        """Return in which place the runner finished."""
        if self.finished(runner):
            return self.finish_list.index(runner)
        return False

    def name(self, place):
        """Return the name of the runner finishing in the given place."""
        # first check that's a valid place (i.e. that many runners have finished the marathon)
        if place <= self.finishers():
            runner_name = self.finish_list[place]
            return runner_name
        return False

    """
    def time(self, place):
        # Return the time of the runner finishing in the given place.
        if place <= self.finishers():
            runner = self.name(place)
            runner_time = self.reg_book[runner]
            return runner_time
        return False
    """

    # Modifiers
    # ---------

    # This modifier is called before the race starts.
    def register(self, runner):
        """Register the runner. Return nothing."""
        time = 0
        self.reg_book[runner] = time

    # This modifier is called after the race starts and before it ends.
    def finish(self, runner, time):
        """Record that the runner just finished the race in the given time.
        Return nothing. Assume the unit of time is seconds.
        """
        self.reg_book[runner] = time
        self.finish_list.append(runner)


"""==================TESTING SECTION=============================="""


def test(name, actual, expected):
    """Print a message if the actual and expected values differ."""
    if actual != expected:
        print(name, ': expected', expected, 'but got', actual)
    else:
        print(name + " : TEST PASSED. " + str(actual))


def populate_marathon(marathon, size, number_of_finishers):
    """Creates marathons filled with dummy data
    for testing purposes"""
    counter = 1
    while counter <= size:
        runner_string = "runnerNo" + str(counter)
        finish_time = 3600 + counter
        marathon.register(runner_string)

        if counter <= number_of_finishers:
            marathon.finish(runner_string, finish_time)

        counter = counter + 1


"""========================================================================="""

print("\n \n")

T1 = 60 * 60  # 1h
T1_01 = T1 + 1  # 1h + 1
T3 = 3 * T1  # 3h
T3_30 = T3 + 30 * 60  # 3h 30min
T4 = 4 * T1  # 4h
T5 = 5 * T1  # 5h

print("======== Milton Keynes Marathon Tests ========== \n")
# The Milton Keynes marathon
mk = Marathon()
mk.register('jane')
mk.register('john')
mk.register('anne')
mk.register('triplet1')  # the triplets are used for testing the marathon ADT can cope
mk.register('triplet2')  # with runners finishing at the exact same time.
mk.register('triplet3')

# these runners register but never finish the race
mk.register('mr lazy')
mk.register('mrs lazy')
mk.register('mr tired')
mk.register('mrs tired')

mk.finish('anne', T1)  # anne comes first with T1 (1h)
mk.finish('john', T1_01)  # then john
mk.finish('jane', T3)  # and jane gets the bronze
mk.finish('triplet1', T3 + 20)
mk.finish('triplet2', T3 + 20)
mk.finish('triplet3', T3 + 20)

print("\n ==== finishers() ==== \n")

test('TEST METHOD: finishers()', mk.finishers(), 6)  # 6 as of 17/3/18 : 10:21

print("\n ==== finishers_up_to() ==== \n")

test('TEST METHOD: finishers_up_to(T4)', mk.finishers_up_to(T4), 6)
print("\n")
test('TEST METHOD: finishers_up_to(T3)', mk.finishers_up_to(T3), 3)
print("\n")
test('TEST METHOD: finishers_up_to(T1 + 10)', mk.finishers_up_to(T1 + 10), 2)
print('\n')

# test finishers_up_to on the triplets, (runners finish at the exact same time).

test('TEST METHOD: finishers_up_to(T3 + 20)', mk.finishers_up_to(T3 + 20), 6)  # test method on exact time.
print("\n")
test('TEST METHOD: finishers_up_to(T3 + 21)', mk.finishers_up_to(T3 + 21), 6)  # test method on boundary above
print("\n")
test('TEST METHOD: finishers_up_to(T3 + 19)', mk.finishers_up_to(T3 + 19), 3)  # test method on boundary below

print("\n ========== name() ========= \n")
"""
test('TEST METHOD: name(1) .. gold', mk.name(1), 'anne')
test('TEST METHOD: name(2) .. silver', mk.name(2), 'john')

print("\n ========== time() ========= \n")

test('TEST METHOD: time(1)', mk.time(1), T1) #time of first place
test('TEST METHOD: time(2)', mk.time(2), T1_01) #time of second place

print("\n =========registered() ======= \n")

test('TEST METHOD: registered(anne)', mk.registered('anne'), True)
test('TEST METHOD: registered(mrs unregistered)', mk.registered('mrs unregistered'), False)
test('TEST METHOD: registered(john)', mk.registered('john'), True)
test('TEST METHOD: registered(adam)', mk.registered('adam'), False)

print("\n ========== finished() ========= \n")

test('TEST METHOD: finished(john)', mk.finished('john'), True)
test('TEST METHOD: finished(mr lazy)', mk.finished('mr lazy'), False)

print("\n ========== place() ========= \n")

test('TEST METHOD: place(jane)', mk.place('jane'), 3)
test('TEST METHOD: place(anne)', mk.place('anne'), 1)

print('======================================')

print('Finish List')

finishcount = 0
for i in mk.finish_list:
    print(type(i))
    print(str(finishcount) + " " + i)
    finishcount = finishcount + 1

print('=== CONSTANTS === \n')
#Test constants
# print("T3 : " + str(T3))
# print("T3 + 19 : " + str(T3 + 19))
# print("T3 + 20 : " + str(T3 + 20))
# print("T3 + 21 : " + str(T3 + 21))

# print('Finish List 0: ' + str(mk.finish_list[0]['time']))
# extractedVariable = mk.finish_list[0]
# print(str(extractedVariable))"""

print('\n ======== NN Marathon Tests ========== \n')

nn = Marathon()
populate_marathon(nn, 100, 50)

"""test finishers_up_to() (binary search) can handle runners finishing
at the same time. """

print(str(nn.finish_list))

nn.register('dupli1')
nn.register('dupli2')
nn.register('dupli3')

nn.finish('dupli1', T3)  # 51
nn.finish('dupli2', T3)  # 52
nn.finish('dupli3', T3)  # 53

nn.register('twin1')
nn.register('twin2')

nn.finish('twin1', T3 + 89)
nn.finish('twin2', T3 + 89)

test('TEST finishers_up_to (2 duplicates at end of list)', nn.finishers_up_to(T3 + 89), nn.finishers())

nn.register('endperson')
nn.finish('endperson', T3 + 100)

test('TEST finishers_up to (2 duplicates within list)', nn.finishers_up_to(T3 + 89), 55)

# make sure duplicate detector in finishers_up_to() works when duplicates not right at the end
"""nn.register('enderman')
nn.register('enderman2')

nn.finish('enderman', T3 + 60)
nn.finish('enderman2', T3 + 70)
"""

test('TEST METHOD: finishers()', nn.finishers(), 53)
test('TEST METHOD: finishers_up_to(T3)', nn.finishers_up_to(T3), 53)

print('\n')
# print(nn.marathon)
# print(str(nn.finish_list))
# print('\n')

"""
#boundary tests .name() function on marathon with 50 finished runners
test('TEST METHOD: name(runnerNo49)', nn.name(49), 'runnerNo49')
test('TEST METHOD: name(runnerNo50)', nn.name(50), 'runnerNo50')
test('TEST METHOD: name(runnerNo51)', nn.name(51), False)
test('TEST METHOD: name(dupli3', nn.name(53), 'dupli3')"""

# print('\n')

# nn.register('first runner')
# nn.finish('first runner', T1)

# print("NN Finish List" + str(nn.finish_list))

# boundary tests .place() method on marathon with 50 finished runners
# test('TEST METHOD: place(49)', nn.place('runnerNo49'), 49)
# test('TEST METHOD: place(50)', nn.place('runnerNo50'), 50)
# test('TEST METHOD: place(51)', nn.place('runnerNo51'), False)

# print('\n')

# test('TEST METHOD: finishers_up_to(T1 + 20)', nn.finishers_up_to(T1 + 20), 20)

# double check that finishers_up_to go the right number
# print(nn.time())

print("REG_BOOK FOR NN MARATHON : " + str(nn.reg_book))
