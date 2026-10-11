# Suggest Pub Decision Document

## Summary

### Challenge

Api calls turned out to be more expensive (monetarily) than first conceived. Minimising api calls for a user search will be key. This will require as much pre-compute as possible to minimise cost. Exact cost TBD.

### Solution

We will develop a general purpose algorithm and a specific 2-person group algorithm. The 2 person algorithm can be seperate as due to two users, its important for the user to feel a rapid response time and know a sensible pub has been suggested, or else trust in the service will decrease. Also there only being two people makes it cheap to do.

The first iteration of the general propose algorithm will userBayesian Inference. It is the only option that will provide a good solution not stuck in local minima while having the potential to have mostly pre-compute and little real time api usage.

The 2-person solution will be developed in stages. Stage:

1. Suggest the pub in the middle of the two people.
2. Use simulated annealing to pick a suitable pub. Hope is this will require a sufficiently small number of iterations and therefore real time API calls.

## Problem and Assumptions Definition

The aim of this app is to suggest pubs to groups of users based on their chosen location. Initially, I will reduce the solution space for simplicity of development and to allow comparison between methods and algorithms.

First, we will only be looking at pubs in London. ChatGPT suggests there are approximately 3,500 pubs in London. Ultimately, I would like to extend the functionality to other cities and areas, and consider venues beyond just pubs.

In theory, groups could be of any size. For algorithm comparison, I will assume a size of 4, which is non-trivial and likely representative of the future average group size.

Ultimately, I would like to fine-tune the algorithm to prioritize different characteristics of pubs (e.g., quality of food), filter the pubs (e.g., closing times, dog-friendly), and compute different modes of transport for the users. These add significant complexity to the algorithm, so most of these features will be included down the line.

API COST ADD HERE WHEN CALCULATED. For algorithm comparison, I will assume a cost of XXXXp per call. A call involves calculating the journey time between two points for a single mode of transport.

Summary: Our aim is to suggest a suitable pub for 4 users located within Greater London, chosen from the ~3,500 total pubs in London. A suitable pub will primarily be defined by minimal total journey time for the group. Other factors include fairness of journey time distribution and pub quality (i.e., rating).

## Options considered

The detailed algorithm comparison, maths notation, and simulated annealing notes are recorded in [`../algorithms/suggest-pub-algorithms.md`](../algorithms/suggest-pub-algorithms.md).
