## 2024-05-18 - [O(N^2) list.index in batch processing]
**Learning:** Found `list.index(item)` inside a loop iterating over batches from the same list, causing $O(N^2)$ complexity.
**Action:** Zip the parallel list (e.g. `batch_texts`) directly to access corresponding elements in $O(1)$ time.
