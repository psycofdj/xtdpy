# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import textwrap
import optparse

#------------------------------------------------------------------#

class IndentedHelpFormatterWithNL(optparse.IndentedHelpFormatter):
  def __init__(self):
    optparse.IndentedHelpFormatter.__init__(self, max_help_position=40)

  def format_description(self, description):
    if not description:
      return ""
    l_descWidth = self.width - self.current_indent
    l_indent = " " * self.current_indent
    # the above is still the same
    l_bits = description.split('\n')
    l_formattedBits = [
      textwrap.fill(bit,
                    l_descWidth,
                    initial_indent=l_indent,
                    subsequent_indent=l_indent)
      for bit in l_bits]
    return "\n".join(l_formattedBits) + "\n"

  def format_option(self, p_option):
    # The help for each option consists of two parts:
    #   * the opt strings and metavars
    #   eg. ("-x", or "-fFILENAME, --file=FILENAME")
    #   * the user-supplied help string
    #   eg. ("turn on expert mode", "read data from FILENAME")
    #
    # If possible, we write both of these on the same line:
    #   -x    turn on expert mode
    #
    # But if the opt string list is too long, we put the help
    # string on a second line, indented to the same column it would
    # start in if it fit on the first line.
    #   -fFILENAME, --file=FILENAME
    #       read data from FILENAME
    l_result = []
    l_opts = p_option.get_opt_string()
    if p_option.metavar:
      l_opts = "%s=%s" % (l_opts, p_option.metavar)
    l_optWidth = self.help_position - self.current_indent - 2
    if len(l_opts) > l_optWidth:
      l_opts = "%*s%s\n" % (self.current_indent, "", l_opts)
      l_indentFirst = self.help_position
    else: # start help on same line as opts
      l_opts = "%*s%-*s  " % (self.current_indent, "", l_optWidth, l_opts )
      l_indentFirst = 0
    l_result.append(l_opts)
    if p_option.help:
      l_helpText = p_option.help
      # Everything is the same up through here
      l_helpLines = []
      l_helpText = "\n".join([x.strip() for x in l_helpText.split("\n")])
      for c_para in l_helpText.split("\n\n"):
        l_helpLines.extend(textwrap.wrap(c_para, self.help_width))
        if len(l_helpLines):
          # for each paragraph, keep the double newlines..
          l_helpLines[-1] += ""
          # Everything is the same after here
      l_result.append("%*s%s\n" % (l_indentFirst, "", l_helpLines[0]))
      l_result.extend(["%*s%s\n" % (self.help_position, "", c_line) for c_line in l_helpLines[1:]])
    elif l_opts[-1] != "\n":
      l_result.append("\n")
    return "".join(l_result)
