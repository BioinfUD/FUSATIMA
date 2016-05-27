/*
  Copyright (c) 2009 Sascha Steinbiss <steinbiss@zbh.uni-hamburg.de>
  Copyright (c) 2009 Center for Bioinformatics, University of Hamburg

  Permission to use, copy, modify, and distribute this software for any
  purpose with or without fee is hereby granted, provided that the above
  copyright notice and this permission notice appear in all copies.

  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/

#ifndef MSORT_API_H
#define MSORT_API_H

#include <stdlib.h>
#include "core/fptr_api.h"

/* Msort module */

/* Sorts an array of <nmemb> elements, each of size <size>, according to compare
   function <compar>. Uses the merge sort algorithm, the interface equals
   <qsort(3)>. */
void gt_msort(void *base, size_t nmemb, size_t size, GtCompare compar);

/* Identical to <gt_msort()> except that the compare function is of
   <GtCompareWithData> type accepting <comparinfo> as arbitrary data. */
void gt_msort_r(void *base, size_t nmemb, size_t size, void *comparinfo,
                GtCompareWithData compar);

#endif
