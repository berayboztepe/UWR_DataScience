using System;
using System.Collections.Generic;

class Program
{
    const int MOD = 1000000007;
    static int cycleCount;
    static List<int> cycleSizes = new List<int>();
    static long result = 1;

    static void ExploreCycle(int node, int[] states, int[] mapping)
    {
        cycleSizes[cycleCount]++;
        states[node] = 3;
        int nextNode = mapping[node];
        if (states[nextNode] != 3)
        {
            ExploreCycle(nextNode, states, mapping);
        }
    }

    static void FindCycles(int node, int[] states, int[] mapping)
    {
        states[node] = 2;
        int nextNode = mapping[node];
        if (states[nextNode] == 0)
        {
            FindCycles(nextNode, states, mapping);
        }
        else if (states[nextNode] == 1)
        {
            states[node] = 1;
            return;
        }
        else
        {
            cycleSizes.Add(0);
            ExploreCycle(node, states, mapping);
            cycleCount++;
        }
        states[node] = 1;
    }

    static void CalculateRoads(int numNodes, int[] connections)
    {
        long[] powerOfTwo = new long[numNodes + 1];
        powerOfTwo[0] = 1;
        for (int i = 1; i <= numNodes; i++)
        {
            powerOfTwo[i] = (powerOfTwo[i - 1] * 2) % MOD;
        }

        int[] states = new int[numNodes + 1];

        for (int i = 1; i <= numNodes; i++)
        {
            if (states[i] == 0)
            {
                FindCycles(i, states, connections);
            }
        }

        int remainingNodes = numNodes;
        foreach (int size in cycleSizes)
        {
            remainingNodes -= size;
            result = (result * (powerOfTwo[size] - 2 + MOD)) % MOD;
        }

        result = (result * powerOfTwo[remainingNodes]) % MOD;

        Console.WriteLine(result);
    }

    static void Main(string[] args)
    {
        int numNodes = int.Parse(Console.ReadLine());
        int[] connections = new int[numNodes + 1];
        string[] input = Console.ReadLine().Split(' ');
        for (int i = 1; i <= numNodes; i++)
        {
            connections[i] = int.Parse(input[i - 1]);
        }

        CalculateRoads(numNodes, connections);
    }
}
