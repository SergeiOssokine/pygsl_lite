/* -*- C -*- */
/**
 * author: Pierre Schnizer
 */
%module _callback

%include typemaps.i
%include constraints.i
%include gsl_function_typemaps.i
%include gsl_error_typemap.i


%include gsl_block_typemaps.i
%{
#include <pygsl_lite/error_helpers.h>
#include "function_helpers.c"
#include "chars.c"
%}

typedef unsigned int size_t;
%init %{
  /* To use the numeric extension */
  init_pygsl_lite();
%}

/* add functions to allocate and free the memory stored by gsl_function */
%inline %{
  gsl_function * gsl_function_init(gsl_function * STORE)
  {
    return STORE;
    /* Do Not need to do anything here. All done in the typemaps */
  }
  gsl_function_fdf * gsl_function_init_fdf(gsl_function_fdf * STORE)
  {
    return STORE;
    /* Do Not need to do anything here. All done in the typemaps */
  }

  void gsl_function_free(gsl_function * FREE)
  {
    /* Do Not need to do anything here. All done in the typemaps */
    DEBUG_MESS(2, "Freeing gsl_function struct %p", (void *) FREE);
  }
  void gsl_function_free_fdf(gsl_function_fdf * FREE)
  {
    /* Do Not need to do anything here. All done in the typemaps */
    DEBUG_MESS(2, "Freeing gsl_function_fdf struct %p", (void *) FREE);
  }

%}


%immutable;
/*
 * Some functions here return int so I have to select the functions which use
 * the returned integer as an error flag
 */



%typemap (out) int = gsl_error_flag;
%include gsl_roots.i
%include gsl_multiroots.i
%include gsl_odeiv.i
 /*
  * %include gsl_multifit.i
  */
