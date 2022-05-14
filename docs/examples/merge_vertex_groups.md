# Merge Vertex Groups
## Accessing
From Object mode, select the objects you want to edit, and go to `Object > Apply > Merge Vertex Groups`.
The operation should apply to all possible objects it can, which is useful for multi-mesh character rigs.

Or, if you're in Weight Paint Mode, simply go to `Weights > Merge Vertex Groups`.
This will allow real-time view of the operation if you make changes after applying it.
You can only do one object at a time with this method.

## Utilization
You should get a menu like this:

![](../images/exmp_mergevertgroups5.png)

From here, fill out the names of the desired vertex groups you want to work with.
If you want to use a constant, select 'Use Constant' and choose where in the formula you want it to be used.
Then set the constant value. The constant value can be any float value--it is not clamped to 0 or 1.

Finally, select your operation. If you want to see what the formula looks like for each one, simply hover your mouse over the option.

![](../images/exmp_mergevertgroups4.png)

## Example
![](../images/exmp_mergevertgroups1.png)

![](../images/exmp_mergevertgroups2.png)

![](../images/exmp_mergevertgroups3.png)