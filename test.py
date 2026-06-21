# %% 
print("calculator coming soon")
# This is a normal code cell
x = 5
y = 10
print(x + y)
# %% [markdown]
# #### Brute force - this is just a test for notes making inside .py
# Time complexity: O(n^2), Space: O(1)
# Walking through nested loops to find the pair.
# **bold**, - bullet, `inline code`, even [links] www.google.com 
# — handy for things like writing **Time:** O(n²) 
# or a bullet list of edge cases you're tracking for a problem.
# %%
# %%
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

print(two_sum([2, 7, 11, 15], 9))
# %% [markdown]
# %% [markdown]
# ## Two Sum
# Reference: [LeetCode #1](https://leetcode.com/problems/two-sum/)
#
# Approach explained here: [Google](https://www.google.com)

# %%
