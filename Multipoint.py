class NPS(object):

    def __init__(self, data, _depth=0):

        if data:
            # Selection of axis on basis of depth which cycles through all the possible values
            self.axis = _depth % len(data[0])


            # Sort point list and choose median as pivot element
            data = sorted(data, key=lambda point: point[self.axis])
            median = len(data) // 2 # choose median

            # Creation of node and construction of subtrees happens here
            self.location = data[median]
            self.child_left = NPS(data[:median], _depth + 1)
            self.child_right = NPS(data[median + 1:], _depth + 1)
        else:
            self.axis = 0
            self.location = None
            self.child_left = None
            self.child_right = None

    def nearest_point(self, point, current_best=None):

        if self.location is None:
            return current_best

        if current_best is None:
            current_best = self.location

        # consider the current node
        if distance(self.location, point) < distance(current_best, point):
            current_best = self.location

        # search the near branch
        current_best = self._child_near(point).nearest_point(point, current_best)

        # search the away branch - maybe
        if self._distance_axis(point) < distance(current_best, point):
            current_best = self._child_away(point).nearest_point(point, current_best)

        return current_best

    # internal methods

    def __repr__(self):
        """
        Simple representation for doctests
        """
        if self.location:
            return "(%d, %s, %s, %s)" % (self.axis, repr(self.location), repr(self.child_left), repr(self.child_right))
        else:
            return "None"

    def _distance_axis(self, point):

        # project point onto node axis
        # i.e. want to measure distance on axis orthogonal to current node's axis
        axis_point = list(point)
        axis_point[self.axis] = self.location[self.axis]
        return distance(tuple(axis_point), point)

    def _child_near(self, point):
        """
        Either left or right child, whichever is closest to the point
        """
        if point[self.axis] < self.location[self.axis]:
            return self.child_left
        else:
            return self.child_right

    def _child_away(self, point):
        """
        Either left or right child, whichever is furthest from the point
        """
        if self._child_near(point) is self.child_left:
            return self.child_right
        else:
            return self.child_left

# helper function

def distance(a, b):
    """
    Squared distance between points a & b
    """
    return (a[0]-b[0])**2 + (a[1]-b[1])**2



def main():


    print "Please enter the number of users(latitude) you want to enter"
    number = int(raw_input())
    lats_input = []
    sum = 0
    for i in range(number):
        lats = raw_input()
        lats_input.append(lats)
        sum = sum + float(lats_input[i])

    x = sum/number
    print x

    print "Please enter the users(longitude) you want to enter"
    longs_input = []
    add = 0
    for i in range(number):
        longs = raw_input()
        longs_input.append(longs)
        add = add + float(longs_input[i])

    y = add/number

    print x,y


    import json

    with open('events.json') as data_file:

       info = json.load(data_file)

    dataset = []
    idset = []


    for event in info["activities"]:
          #tuple (lat.lng)

          if len(event["latitude"]) > 0 and len(event["longitude"]) > 0:
              item = (float(event["latitude"]), float(event["longitude"]))
              dataset.append(item)

          if len(event["itid"]) > 0:
            id = str(event["itid"])

            idset.append(id)



    print idset


    d = (x,y)

    w = []
    idsetnew = []


    s = dataset

    print "Number of events? : "
    num = int(raw_input())
    for i in range(num):

        tree = NPS(s)
        a = tree.nearest_point(d)
        index = s.index(a)
        popped = s.pop(index)
        indexid = index
        poppedid = idset[indexid]
        w.append(popped)
        idsetnew.append(poppedid)

    print w
    print idsetnew


    f = open("pythondata.js", "w")
    totalevents = []
    for x in s:
        totalevents.append("['otherevents' , " + str(x[0]) + ", " + str(x[1]) + "]");
    totaleventsStr = ",".join(totalevents)

    finaldata = []
    for latLng in w:

        finaldata.append(str(latLng[0]) + ", " +str(latLng[1]))

    finaldataStr = ",".join(finaldata)

    finaldatas = []
    for k in range(0, num):
        finaldatas.append("[" + "'" + idsetnew[k] + "'" + ", " + finaldata[k] + " ]");
    finaldatasStr = ",".join(finaldatas)

    userLocations = []
    for i in range(0, number):
        userLocations.append("[ 'user', " + str(lats_input[i]) + ", " + str(longs_input[i]) + "]");

    userLocationsStr = ",".join(userLocations)
    f.write("var nearest_events = [" + finaldatasStr + "];\n")
    f.write("var totalevents = [" + totaleventsStr + "];\n")
    f.write("var user_position = [" + userLocationsStr + "];\n")

    f.close()


if __name__ == '__main__':
    main()

