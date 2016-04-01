# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"
__copyright__ = "http://stackoverflow.com/questions/20656135/python-deep-merge-dictionary-data"

#------------------------------------------------------------------#

def mergedicts(p_dict1, p_dict2):
  for k in set(p_dict1.keys()).union(p_dict2.keys()):
    if k in p_dict1 and k in p_dict2:
      if isinstance(p_dict1[k], dict) and isinstance(p_dict2[k], dict):
        yield (k, dict(mergedicts(p_dict1[k], p_dict2[k])))
      else:
        # If one of the values is not a dict, you can't continue merging it.
        # Value from second dict overrides one in first and we move on.
        yield (k, p_dict2[k])
        # Alternatively, replace this with exception raiser to alert you of value conflicts
    elif k in p_dict1:
      yield (k, p_dict1[k])
    else:
      yield (k, p_dict2[k])

#------------------------------------------------------------------#
