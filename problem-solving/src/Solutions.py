# DO NOT ADD ANY IMPORTS
from typing import *


class Solutions:
    # DO NOT MODIFY INIT
    def __init__(self):
        pass

    # Problem 1: Real Estate Profits
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm uses a DP approach, recursively computing the maximum possible profit by
    # considering all possible sequences of selling the property and storing the one that
    # gives the highest profit in the DP table. Considering the case where there are no neighbors
    # of a property (the out of bounds within the problem description), the numbers array is padded
    # with 1 on both ends. The recursive function maximumProfit(left, right) calculates the max
    # profit that can be obtained from selling properties between indices left and right by choosing
    # each property i within the range  as the next to sell and combining the profits from the resulting
    # subproblems. Memoization through the DP array ensures that overlapping subproblems are solved
    # only once, guaranteeing correctness and efficiency.
    #
    # Runtime:
    # The overall runtime of this algorithm is O(n^3), where n is the number of properties in the input list 'values'.
    # There are O(n^2) possible combinations of pairs of left and right values, and the
    # algorithm iterates up to O(n) possible solutions of i to consider as the next property to sell.
    #
    # Therefore, O(n^3).
    #
    def realEstatePrices(values: List[int]) -> int:
        # accounting for base case: property doesnt have neighbors, we're padding them with 1
        numbers = [1] + values + [1]
        n = len(numbers)
        dp = [[-1] * n for _ in range(n)]

        def maximumProfit(left: int, right: int) -> int:
            # accounting for base case of 0 properties left to sell
            if left + 1 == right:
                return 0

            if dp[left][right] != -1:
                return dp[left][right]

            maxProfit = 0

            # attempt selling property between left & right
            for i in range(left + 1, right):
                profit = numbers[left] * numbers[i] * numbers[right]
                totalProfit = profit + maximumProfit(left, i) + maximumProfit(i, right)
                maxProfit = max(maxProfit, totalProfit)

            dp[left][right] = maxProfit

            return maxProfit

        # maximumProfit(0, n-1)
        # return dp[n - 1]          # this works too

        return maximumProfit(0, n - 1)

    # Problem 2: Warehouse Package Stacking
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm calculates the maximum number of maximum number of packages that can be
    # stacked by transforming the problem into finding the longest increasing subsequence (LIS)
    # of package heights. First, it sorts the packages by width in ascending order, and for
    # packages with the same width, they are sorted by height in descending order. This sorting
    # ensures that when widths are equal, a larger height cannot erroneously be considered
    # stackable over a smaller one. After sorting, it gets the heights and performs LIS
    # using binary search, which effectively identifies the maximum number of packages that
    # can be stacked according to the strictly smaller-than requirement for both width and height.
    #
    # Runtime:
    # The overall runtime of this algorithm is O(n log(n)), where n is the number of packages.
    # The sorting of the packages is assumed O(n log(n)), and finding the LIS using binary
    # search is also O(n log(n)). They are done separately.
    #
    # Therefore, O(n log(n)).
    #
    def maxPackages(packages: List[Tuple[int, int]]) -> int:
        # sort the packages by width, then height in descending order
        # assuming O(n log(n))
        packages.sort(key=lambda x: (x[0], -x[1]))

        heights = [p[1] for p in packages]

        # find longest increasing subsequence
        dp = []
        for height in heights:
            left, right = 0, len(dp)
            while left < right:
                mid = (left + right) // 2
                if dp[mid] < height:
                    left = mid + 1
                else:
                    right = mid

            if left < len(dp):
                dp[left] = height
            else:
                dp.append(height)

        return len(dp)

    # Problem 3: Building Blocks
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm correctly computes the minimum number of swaps needed to make both
    # sequenced strictly increasing with a DP solution. It keeps 2 arrays, keep and swap
    # where keep[i] represents the minimum number of swaps needed to keep the elements at
    # index i unchanged, and swap[i] represents the minimum number of swaps needed when
    # swapping the elements at index i. At each index, the algorithm checks two conditions:
    # whether keeping or swapping the current elements maintains the order based on the
    # previous elements. This ensures that the sequences remain strictly increasing.
    # By updating the keep and swap array with the minium swaps needed under these conditions,
    # the algorithm checks all valid possibilities, ensuring an optimal solution.
    # If there is no valid sequence possible, it returns -1.
    #
    # Runtime:
    # The overall runtime of this algorithm is O(n), where n is the length of the input arrays.
    # This is because the algorithm iterates through the arrays once, performing O(1) operations
    # at each index.
    #
    # Therefore, O(n).
    #
    def minSwap(nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)

        swap = [float("inf")] * n
        keep = [float("inf")] * n

        # base case
        swap[0] = 1
        keep[0] = 0

        for i in range(1, n):
            if nums1[i] > nums1[i - 1] and nums2[i] > nums2[i - 1]:
                keep[i] = keep[i - 1]
                swap[i] = swap[i - 1] + 1

            if nums1[i] > nums2[i - 1] and nums2[i] > nums1[i - 1]:
                keep[i] = min(keep[i], swap[i - 1])
                swap[i] = min(swap[i], keep[i - 1] + 1)

        result = min(keep[-1], swap[-1])
        return result if result != float("inf") else -1

    # Problem 4: Modular Two Sum
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm efficiently counts all pairs of integers which sum is divisible by k
    # by using modulo. First, it calculates the frequency of each possible remainder when the
    # elements from the list are divided by k, and store these in an array 'counts' of size k.
    # As two numbers sum to a multiple of k if and only if their remainders sum to k or modulo k,
    # the algorithm pairs each remainder with its complement k - remainder to count the number
    # of valid pairs. Special cases where the remainder is 0 or even are handled separately
    # because they can only pair with themselves to sum to a multiple of k. By calculating the
    # number of pairs for each remainder, this algorithm ensures all valid pairs are counted
    # exactly once, which guarantees correctness.
    #
    # Runtime:
    # The runtime of this algorithm is O(n + k), where n is the number of elements in the input
    # 'nums' list and k the input divisor k.
    # Calculated the remainders and each frequencies takes O(n).
    # Iterating through the possible remainders to compute the pair counts takes O(k).
    #
    # Therefore, O(n + k)
    #
    def modTwoSum(nums: List[int], k: int) -> int:
        counts = [0] * k  # store counts of remainders

        # calculate remainders and update counts
        for num in nums:
            remainder = num % k
            counts[remainder] += 1

        numPairs = 0

        # handle pairs where both numbers have remainder 0
        numPairs += counts[0] * (counts[0] - 1) // 2

        # handle remainders from 1 to k // 2 - 1
        for remainder in range(1, (k + 1) // 2):
            complement = k - remainder
            numPairs += counts[remainder] * counts[complement % k]

        # if k is even, handle the special case where remainder equals k // 2
        if k % 2 == 0:
            remainder = k // 2
            numPairs += counts[remainder] * (counts[remainder] - 1) // 2

        return numPairs

    # Problem 5: Maximum Magic Path Power
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm correctly computes the maximum possible power of any valid journey
    # by performing BFS with customized states. Each state in the BFS is defined
    # by the current location, time taken so far, the total energy collected, and a bitmask
    # representing the set of unique locations visited. By exploring all possible paths possible'
    # during the 'maxTime', the algorithm ensures that every valid journey started and ending at
    # location 0 is considered. The use of the DP table lets the algorithm avoid redundant
    # calculations by skipping states that have already been visited with less or equal time.
    # This guarantees that the maximum energy collected is accurately tracked and updated
    # whenever a valid journey returns to the starting point.
    #
    # Runtime:
    # The runtime of this algorithm is O(n * 2^n), where n is the number of locations.
    # This is because in the worst case the algorithm needs to consider all possible
    # subsets of locations for each node due to the visited bitmask. The number of location
    # states can be up to n * 2^n, and each location is connected by at most four paths.
    # Thus, O(4 * n * 2^n) = O(n * 2^n). Constructing the graph is O(n), because of the
    # edges of each node is constrained to 4 edges. Updating the DP table only takes O(1).
    #
    # Therfore, O(n * 2^n).

    def maximumMagicPathPower(
        energies: List[int], edges: List[List[int]], maxTime: int
    ) -> int:
        n = len(energies)

        # build adjacency list
        graph = {}
        for u, v, time in edges:
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append((v, time))
            graph[v].append((u, time))  # since paths are bidirectional

        # initialize bfs queue
        queue = []
        startEnergy = energies[0]
        startState = (
            0,
            0,
            startEnergy,
            1 << 0,
        )  # (currentTime, currentNode, collectedEnergy, visitedMask)
        queue.append(startState)

        # dictionary to store minimum time to reach (node, visitedMask)
        dp = {}
        dp[(0, 1 << 0)] = 0

        maxEnergyCollected = startEnergy if maxTime >= 0 else 0

        while queue:
            # dequeue the first element
            currentTime, currentNode, collectedEnergy, visitedMask = queue.pop(0)

            # explore neighbors
            if currentNode in graph:
                for neighbor, edgeTime in graph[currentNode]:
                    newTime = currentTime + edgeTime
                    if newTime > maxTime:
                        continue

                    # check if the neighbor has been visited
                    hasVisited = visitedMask & (1 << neighbor)
                    newCollectedEnergy = collectedEnergy
                    newVisitedMask = visitedMask
                    if not hasVisited:
                        newCollectedEnergy += energies[neighbor]
                        newVisitedMask |= 1 << neighbor

                    # skip if already reached this state with less or equal time
                    dpKey = (neighbor, newVisitedMask)
                    if dpKey in dp and dp[dpKey] <= newTime:
                        continue

                    dp[dpKey] = newTime

                    # if we return to node 0, update the maximum energy collected
                    if neighbor == 0:
                        maxEnergyCollected = max(maxEnergyCollected, newCollectedEnergy)

                    # enqueue the new state
                    queue.append(
                        (newTime, neighbor, newCollectedEnergy, newVisitedMask)
                    )

        return maxEnergyCollected

    # Problem 6: Divide the Harvest
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm correctly computes the highest possible quantity of fruit you can keep by maximizing
    # the minimal sum among all possible partitions and then selecting the second smallest portion.
    # The algorithm uses binary search to find the largest minimal sum 'minSum' such that the array can be
    # divided into exactly k + 1 contiguous portions with each portion's sum being at least 'minSum'.
    # The helper function 'canPartition' checks if a given minSum is feasible by greedily accumulating
    # basket quantities and making cuts when the accumulated sum reaches or exceeds minSum, ensuring
    # all portions meet the minimal sum requirement. By iteratively adjusting minSum through binary
    # search and updating the answer when a valid partition is found, the algorithm ensures it finds the
    # maximum possible minimal sum. Finally, it selects the second smallest portion sum from the valid
    # partition, fulfilling the condition of taking the second-smallest portion after dividing.
    #
    # Runtime:
    # The runtime of the algorithm is O(n log(S)), where n is the number of baskets and S is the total sum of quantities.
    # The binary search in this algorithm operates in O(log(S)) time, and each call to 'canPartition' runs in O(n) time.
    #
    # Therefore, O(n log(S)).
    #
    def divideTheHarvest(quantity: List[int], k: int) -> int:
        n = len(quantity)

        # function to check if it's possible to partition the array with minimum sum 'M'
        def canPartition(minSum: int) -> List[int]:
            portions = []
            accumulated = 0
            cutsMade = 0

            for i in range(n):
                accumulated += quantity[i]
                # make a cut if accumulated sum >= minSum and we have cuts remaining
                if accumulated >= minSum and cutsMade < k:
                    portions.append(accumulated)
                    accumulated = 0
                    cutsMade += 1
            # add the last portion
            portions.append(accumulated)

            # check if we have exactly k + 1 portions and all portions meet the minSum requirement
            if len(portions) != k + 1 or min(portions) < minSum:
                return []
            return portions

        # binary search to find the maximum possible minimal sum
        left, right = min(quantity), sum(quantity)
        answerPortions = []
        while left <= right:
            mid = (left + right) // 2
            portions = canPartition(mid)
            if portions:
                # if possible, try for a higher minimal sum
                left = mid + 1
                answerPortions = portions
            else:
                right = mid - 1

        # after finding the maximum minimal sum, extract the second smallest portion sum
        if not answerPortions:
            return 0  # edge case if partitioning is not possible

        sortedPortions = sorted(answerPortions)

        # get the second smallest portion sum
        secondMinSum = (
            sortedPortions[1] if len(sortedPortions) > 1 else sortedPortions[0]
        )

        return secondMinSum

    # Problem 7: Coloring Sidewalks
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm calculates the minimum total time required to paint all sidewalks such that
    # no two adjacent sidewalks share the same color using a DP solution. The dp array is initialized
    # to keep track of the minimum time to paint up to each sidewalk with each color. dp[i][c] represents
    # the minimum time to paint side walks from index 0 to i with sidewalk i painted in color c.
    # At each side walk i, the algorithm considers painting it with each of the 3 colors (gold, white, blue).
    # For each color choice, it adds the time required to apint the current sidewalk that color to the minimum
    # of the total times from painting the previous sidewalk with a different color. This ensures that the
    # constraints of no adjacent sidewalks cannot be the same color.
    #
    # Runtime:
    # The time complexity of this algorithm is O(n), where n is the number of sidewalks.
    # As the number of colors is a constant 3, the operations for each sidewalk takes O(1).
    # This includes the addition of the current painting time time[i][c] and finding the minimum between
    # two previous dp values min(dp[i - 1][c']). This is done for every sidewalk, thus O(n).
    #
    # Therefore, O(n).
    #
    def coloringSidewalks(time: List[int]) -> int:
        n = len(time)
        # initialize dp array: dp[i][c] represents the minimum time to paint up to sidewalk i with color c
        dp = [[0] * 3 for _ in range(n)]

        # base case: the cost to paint the first sidewalk with each color
        dp[0][0] = time[0][0]  # gold
        dp[0][1] = time[0][1]  # white
        dp[0][2] = time[0][2]  # blue

        for i in range(1, n):
            # paint current sidewalk with gold
            dp[i][0] = time[i][0] + min(
                dp[i - 1][1], dp[i - 1][2]
            )  # cannot be the same as previous color
            # paint current sidewalk with white
            dp[i][1] = time[i][1] + min(dp[i - 1][0], dp[i - 1][2])
            # paint current sidewalk with blue
            dp[i][2] = time[i][2] + min(dp[i - 1][0], dp[i - 1][1])

        # return the minimum total time to paint all sidewalks
        return min(dp[n - 1][0], dp[n - 1][1], dp[n - 1][2])

    # Problem 8: Chemical Concoctions
    # Explanation and Runtime:
    #
    # Explanation:
    # The algorithm determines a valid ordering of the chemicals by constructing a directed graph
    # based on the ordering constraints inferred from the given formulas. It compares adjacent formulas
    # to find the first differing chemicals and creates an edge from the first to the second chemical,
    # indicating that the first must come before the second in the ordering. Then, it performs a topological
    # sort using Kahn's algorithm, starting with chemicals that have zero in-degree, which mean no dependencies,
    # to establish a valid sequence that satisfies all constraints. If it successfully includes all chemicals
    # in the ordering, it returns the concatenated sequence. Otherwise, it returns an empty string,
    # indicating that no valid ordering exists. The use of sorted queues ensures that when multiple chemicals
    # have zero in-degree, the lexicographically smallest one is chosen, which yields any valid ordering.
    #
    # Runtime:
    # The runtime of this algorithm is O(n), where n is the total number of characters in all formulas.
    # This is because we loop through every formula and every character in each formula to populate 'graph' and 'inDegree'
    # The topological sort operates in O(m log(m)), where m is the number of chemicals. However,
    # as the number of chemicals is constrained at most 26, this could be considered constant.
    #
    # Therefore, O(n)
    #
    def chemicalConcoctions(formulas: List[str]) -> str:
        # build the graph
        graph = {}  # adjacency list
        inDegree = {}  # count of incoming edges for each chemical
        nodes = set()  # set of all unique chemicals

        # initialize inDegree and graph for all unique chemicals
        for formula in formulas:
            for c in formula:
                nodes.add(c)
                if c not in inDegree:
                    inDegree[c] = 0
                if c not in graph:
                    graph[c] = []

        # build edges between chemicals based on the formulas' order
        for i in range(len(formulas) - 1):
            word1 = formulas[i]
            word2 = formulas[i + 1]
            minLength = min(len(word1), len(word2))

            for j in range(minLength):
                c1 = word1[j]
                c2 = word2[j]
                if c1 != c2:
                    # if found a difference, add an edge from stars1 to stars2
                    graph[c1].append(c2)
                    inDegree[c2] += 1
                    break  # only the first differing character matters
            else:
                # if word1 is longer than word2 and all previous characters matched, invalid
                if len(word1) > len(word2):
                    return ""

        # topological sort using kahn's algorithm
        # start with chemicals that have zero in-degree
        queue = sorted([node for node in nodes if inDegree[node] == 0])

        order = []
        while queue:
            current = queue.pop(0)
            order.append(current)
            # process neighbors in sorted order
            for neighbor in sorted(graph[current]):
                inDegree[neighbor] -= 1
                if inDegree[neighbor] == 0:
                    queue.append(neighbor)
            # sort the queue
            queue.sort()

        # if can't include all chemicals, there has to be a cycle
        if len(order) != len(nodes):
            return ""

        return "".join(order)

    # Problem 9: Maximum Sum of Non-Adjacent Subsequences
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm efficiently computes the maximum sum of a non-adjacent subsequence by using dynamic programming.
    # It maintains two variables: 'prevMax', representing the maximum sum including the previous element, and 'prevPrevMax',
    # representing the maximum sum excluding the previous element. At each step, the algorithm decides whether to include
    # the current element by comparing 'prevMax' (excluding the current element) and 'prevPrevMax + nums[i]'
    # (including the current element). This ensures that no two adjacent elements are selected, as including the
    # current element skips over the immediate previous one. By iteratively updating these variables, the algorithm
    # builds up the optimal solution, guaranteeing that the maximum possible sum is found without violating the
    # non-adjacency constraint.
    #
    # Runtime:
    # The runtime of the algorithm is O(n), where n is the length of the input array 'nums'.
    # This is because it processes each element exactly once in a single loop, performing O(1) operations
    # such as 'max(prevMax, prevPrevMax + nums[i])' and assigning values on each iteration.
    #
    # Therefore, O(n)
    #
    def maxNonAdjSum(nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        elif n == 1:
            return nums[0]

        # initialize variables to store the maximum sums
        prevPrevMax = 0  # max sum excluding the previous element
        prevMax = nums[0]  # max sum including the previous element

        for i in range(1, n):
            # calculate the new maximum sum by including or excluding the current element
            currentMax = max(prevMax, prevPrevMax + nums[i])
            # update the variables for the next iteration
            prevPrevMax = prevMax
            prevMax = currentMax

        return prevMax

    # Problem 10: DigitGPT
    # Explanation and Runtime:
    #
    # Explanation:
    # The algorithm determines whether Melon will replace Scam as CEO by calculating the potential maximum
    # impact both players can have on the sum difference between the first and second halves of the string.
    # It first computes the sums of the known digits (digitSum1, digitSum2) and counts the number of * symbols
    # (stars1, stars2) in each half. Since both players replace * symbols optimally, the player with more *
    # symbols can manipulate the sum more significantly. The maximum difference achievable is when the player
    # replaces their * symbols with 9s, and the opponent replaces theirs with 0s, resulting in a difference of
    # 9 * (starDiff // 2). The algorithm checks if the existing sum difference matches this maximum possible
    # difference (accounting for which half has more *s), determining if Melon can win under optimal play.
    #
    # Runtime:
    # The runtime of this algorithm is O(n), where n is the length of the 'ticket' string.
    # The algorithm processes each character of the string once to compute the digit sums and * counts,
    # and the comparisons between star numbers and difference calculation is done in O(1).
    #
    # Therefore, O(n).
    #
    def reviveStrings(n: int, ticket: str) -> bool:
        digitSum1, digitSum2 = 0, 0  # sum of digits in first half, second half
        stars1, stars2 = 0, 0  # counts of * in first half, second half

        halfpoint = n // 2  # half point of the ticket

        for i in range(halfpoint):  # start to halfpoint
            if ticket[i] == "*":
                stars1 += 1
            else:
                digitSum1 += int(ticket[i])

        for i in range(halfpoint, n):  # halfpoint to end
            if ticket[i] == "*":
                stars2 += 1
            else:
                digitSum2 += int(ticket[i])

        difference = digitSum1 - digitSum2  # added absolute value.
        starDiff = abs(stars1 - stars2)
        # this made test case: **2641 output a correct answer

        # difference has a sign. so the variance possible with stars must have sign as well
        if stars1 < stars2:
            return difference == 9 * (starDiff // 2)

        elif stars1 > stars2:
            return difference == -9 * (starDiff // 2)

        # if number of stars are the same in first and second half
        elif stars1 == stars2:
            # if digitSum1 == digitSum2: true. else, false. i think this is it
            return difference == 0

        else:  # never will really come to this else statement
            return False

    # Problem 11: Building a Brick Wall
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm calculates the number of unique ways to build a wall of the given length using the
    # available bricks by employing dynamic programming. It initializes a list dp where dp[i] represents
    # the number of ways to construct a wall of length i. Starting from the smallest brick length, it iterates
    # over each brick type and, for each possible wall length from the brick length up to the target length,
    # it updates dp[currentLength] by adding dp[currentLength - brick]. This addition represents the number of
    # ways to reach the current length by adding the current brick to all the ways of building a wall of length
    # currentLength - brick. By building up the solution from smaller lengths to the target length, the algorithm
    # ensures that all possible combinations are counted accurately, guaranteeing correctness.
    #
    # Runtime:
    # The time complexity of the algorithm is O(n * l), where n is the number of brick types and l is the target wall length.
    # This is because the algorithm iterates over each brick type and, for each brick, it processes all wall lengths from the
    # brick's length up to the target length.
    #
    # Therefore, O(n * l).
    #
    def buildBrickWall(bricks: List[int], length: int) -> int:
        # initialize a list to store the number of ways to build walls of length up to 'length'
        dp = [0] * (length + 1)
        dp[0] = (
            1  # base case: there is 1 way to build a wall of length 0 (using no bricks)
        )

        # sort the brick lengths to ensure consistent ordering
        bricks.sort()

        # dynamic programming to compute the number of ways to build walls of each length
        for brick in bricks:
            for currentLength in range(brick, length + 1):
                dp[currentLength] += dp[currentLength - brick]

        return dp[length]

    # Problem 12: Archipelagos
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm correctly identifies all the critical bridges in the archipelago by implementing SCC algorithm
    # for finding bridges in an undirected graph. It performs a depth first search (DFS) traversal, assigning to each
    # node a discovery time 'discoveryTime' and the lowest reachable time 'lowTime' from that node. For each node 'u',
    # it explores all adjacent nodes 'v'. If 'v' hasn't been visited, it recursively calls DFS on 'v' and updates
    # lowTime[u] based on lowTime[v]. If lowTime[v] > discoveryTime[u], it means there's no back edge connecting 'v'
    # or its descendants back to 'u' or its ancestors, indicating that the edge (u, v) is a bridge whose removal
    # would disconnect the graph. By systematically applying this process, the algorithm ensures that all such
    # critical bridges are found, demonstrating its correctness.
    #
    # Runtime:
    # The runtime of this algorithm is  O(n + m), where n is the number of islands (nodes) and m is the number of bridges (edges).
    # This is because it performs a DFS traversal that visits each node once and processes each edge twice (once from each
    # connected node).
    #
    # Therefore, O(n + m).
    #
    def findNeededBridges(
        n: int, edges: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        # build the adjacency list
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)  # since the graph is undirected

        visited = [False] * n
        discoveryTime = [0] * n
        lowTime = [0] * n
        parent = [-1] * n
        time = [0]  # using a list to make time mutable in nested function
        bridges = []

        def dfs(u):
            visited[u] = True
            discoveryTime[u] = lowTime[u] = time[0]
            time[0] += 1

            for v in graph[u]:
                if not visited[v]:
                    parent[v] = u
                    dfs(v)
                    lowTime[u] = min(lowTime[u], lowTime[v])

                    # if the lowest reachable vertex from subtree rooted with v is
                    # below u in dfs tree, then u-v is a bridge
                    if lowTime[v] > discoveryTime[u]:
                        bridges.append((u, v))
                elif v != parent[u]:
                    # update low value of u for parent function calls
                    lowTime[u] = min(lowTime[u], discoveryTime[v])

        # call dfs for each unvisited node
        for i in range(n):
            if not visited[i]:
                dfs(i)

        return bridges

    # Problem 13: Search Engineer
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm calculates the number of distinct subsequences of text that match pattern using dynamic programming.
    # It employs a one-dimensional dp array where dp[j] represents the number of ways the first j characters of pattern
    # can be formed from the characters up to the current position in text. Initially, dp[0] is set to 1 because an empty
    # pattern is a subsequence of any string. The algorithm iterates over each character in text, and for each character,
    # it iterates backward through pattern to update dp[j]. If the current characters in text and pattern match, it adds
    # dp[j - 1] to dp[j], accounting for the new ways the subsequence can be formed with this match. By updating dp in
    # reverse, it ensures that the calculations use the previous state values correctly, and by considering all positions,
    # it accurately counts all distinct subsequences, guaranteeing correctness.
    #
    # Runtime:
    # The runtime of this algorithm is O(n * m), where n is the length of text and m is the length of pattern.
    # The algorithm has a nested loop that iterates through the characters of text and pattern. This results
    # in a total of n * m iterations. The dp array update is done in O(1) time.
    #
    # Therefore, O(n * m).
    #
    def numDistinct(text: str, pattern: str) -> int:
        n = len(text)
        m = len(pattern)

        if m == 0:
            return 1
        if n == 0:
            return 0

        # initialize a 1d dp array
        dp = [0] * (m + 1)
        dp[0] = 1  # empty pattern

        for i in range(1, n + 1):
            # traverse from end to start to not overwrite dp[j - 1] before it's used
            for j in range(m, 0, -1):
                if text[i - 1] == pattern[j - 1]:
                    dp[j] = dp[j - 1] + dp[j]

        return dp[m]

    # Problem 14: Buzz's Bees
    # Explanation and Runtime:
    #
    # Explanation:
    # This algorithm calculates the minimum cost to connect all the bees by implementing Prim's algorithm for
    # finding the minimum spanning tree (MST) of a complete graph formed by the bees. It starts by initializing
    # the minCost array, where minCost[i] represents the minimum cost to connect bee i to the existing network.
    # The algorithm repeatedly selects the unvisited bee with the smallest minCost value, adds it to the network
    # by marking it as visited, and updates the minCost values for the remaining unvisited bees based on the cost
    # to connect them to the newly added bee. The cost between any two bees is calculated using the formula given
    # within the problem, which is the squared Euclidean distance formula (x_i - x_j)^2 + (y_i - y-j)^2, ensuring
    # that all possible connections are considered. By progressively connecting the bees with the minimal additional
    # cost, the algorithm efficiently computes the minimum total cost to establish the bee network.
    #
    # Runtime:
    # The runtime of the algorithm is O(n^2), where n is the number of bees.
    # For each bee, the algorithm searches through all unvisited bees to find the one with the minimum cost and then
    # updates the costs for all other unvisited bees, resulting in n iterations each containing n operations.
    # Calculating the distances using the given formula takes O(1) for each edge during the updates, thus does not
    # alter the overall O(n^2).
    #
    # Therefore, O(n^2).
    #
    def minNetworkCost(coords: List[Tuple[int, int]]) -> int:

        n = len(coords)

        if n == 0:  # handling edge case of empty list of coords
            return 0

        visited = [False] * n
        minCost = [float("inf")] * n
        minCost[0] = 0
        totalCost = 0

        # using prim's algorithm
        for _ in range(n):
            u = -1
            # look for unvisited node with the smallest minCost
            for v in range(n):
                if not visited[v] and (u == -1 or minCost[v] < minCost[u]):
                    u = v

            if minCost[u] == float("inf"):  # this means graph is not connected
                return -1

            visited[u] = True
            totalCost += minCost[u]

            # update the minCost with the costs from the added node
            for v in range(n):
                if not visited[v]:
                    cost = (coords[u][0] - coords[v][0]) ** 2 + (
                        coords[u][1] - coords[v][1]
                    ) ** 2
                    if cost < minCost[v]:
                        minCost[v] = cost

        return totalCost
