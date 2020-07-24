    '''
       10
     /
    1   2   4  11
     \ /   / \ /
      3   5   8
       \ / \   \
        6   7   9
    '''



| Stack | Visited | Explanations |
|-------|-------:|--------------:|
| [6] |     na   | |
| [6,3] [6,5]| [6] | 6 gets copied to make the other 2 |
| [6,5] | [6] [6,3] | 6,3 gets copied, and put back on stack |
| [6,3,1] [6,5] | [6] [6,3] [6,3,1] | 6,3,1 gets copied, and put back on stack |
| [6,3,1,10] [6,5] | [6] [6,3] [6,3,1] [6,3,1,10] | 10 has no child, so doesn't get copied | 
| [6,5] |  [6] [6,3] [6,3,1] [6,3,1,10] | 6,5 gets copied and put back on stack |
| 
