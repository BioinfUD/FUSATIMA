/*
  Copyright (c) 2008-2011 Gordon Gremme <gordon@gremme.org>
  Copyright (c) 2008      Center for Bioinformatics, University of Hamburg

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

#ifndef SA_VISITOR_H
#define SA_VISITOR_H

#include "gth/sa.h"

/* the ``spliced alignment visitor'' interface */
typedef struct GthSAVisitorClass GthSAVisitorClass;
typedef struct GthSAVisitor GthSAVisitor;

void gth_sa_visitor_preface(GthSAVisitor*);
void gth_sa_visitor_visit_sa(GthSAVisitor*, GthSA*);
void gth_sa_visitor_trailer(GthSAVisitor*, GtUword num_of_sas);
void gth_sa_visitor_delete(GthSAVisitor*);

#endif
