# Clean and Combine
In Object mode, select the objects you want to clean and merge, and make the object you want to merge them into Active. Then, go to `Object > Cleanup > Clean and Combine`. Choose the corresponding settings you like. The resulting objects will have modifiers applied or discarded, be joined together, have geometry cleaned using the given settings, and finally have all transforms applied. This operator is great for multi-part characters, or just generally cleaning up messy files before exporting.

Please note that all modifiers are applied or discarded. **THERE WILL BE DATA LOSS**, but **Armatures and bone weights are preserved**. Though the operator can be undone, it is strongly recommended to have a backup of your model, and only use this tool when you are certain that you want to, or are exporting a model.

![](../images/exmp_cleancombine_p1.png)
![](../images/exmp_cleancombine_p2.png)