#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
import sys, os, re
from pyworkdispatcher import Worker, Dispatcher, ValueOption, PositionOption

def check_dir_existance(outp_dir):
    try:
        os.mkdir(outp_dir)
    except OSError, e:
        raise ValueError, "Application is exist in current directory" + str(e)

def copy_lines( path, outp_path, processor = ( lambda line: line ) ):
    inp = open(path, 'r')
    outp = open(outp_path, 'w')
    for line in inp.readlines():
        line = processor( line )
        outp.writelines([line])

def get_outp_dir(app_name, app_dir, d):
    outp_dir = os.path.join(os.getcwd(), app_name, d[len(app_dir) + 1:])
    return outp_dir

def get_app_dir(app_name):
    mod = __import__("turbion.%s" % app_name)
    app_dir = os.path.join(os.path.dirname(mod.__file__), app_name)
    return app_dir

def get_new_name():
    dst_dir = os.getcwd()
    bits = dst_dir.split( os.path.sep )
            
    for i in range( 0, len( bits ) ):
        module_dir = os.path.sep.join( bits[ : -i ] + [ 'settings' ] )

        if os.path.exists( module_dir ) or os.path.exists( module_dir + '.py' ):
            return ".".join( bits[ -i - 1 : ] )
    raise ValueError

def generic_export( app_name, new_name, suffix, processor = lambda line:line ):
    try:
        app_dir = os.path.join( get_app_dir(app_name), suffix )

        for d, subdirs, files in os.walk(app_dir):
            if '.svn' in d:
                continue

            outp_dir = get_outp_dir(app_name, app_dir, d)
            
            check_dir_existance(outp_dir)
            
            for f in files:
                if os.path.splitext( f )[1][1:] in ( 'pyc', ):
                    continue
                path = os.path.join( d, f )
                outp_path = os.path.join( outp_dir, f )

                copy_lines( path, outp_path, processor )

    except ImportError:
        print "No such application: turbion.%s" % app_name

def export( app_name ):
    reg = re.compile("turbion." + app_name)
    new_name = get_new_name() + "." + app_name
    processor = lambda line: reg.sub(lambda match: new_name, line)    
                
    generic_export( app_name, new_name, "", processor)

def export_templates( app_name ):
    new_name = get_new_name() + "." + app_name
    generic_export( app_name, new_name, "templates" )
    
class ConfigWorker( Worker ):
    settings = ValueOption( 's', 'settings' )
    
    def execute( self ):
        if not self.settings:
            return
        from django.core.management import setup_environ
        
        sys.path.append( os.getcwd() )
        
        mod = __import__( self.settings, fromlist = [ "foo" ] )
        setup_environ( mod )
        
        from django.conf import settings
        if hasattr( settings, "PROJECT_ROOT_DIR" ):
            sys.path.append( os.path.dirname( settings.PROJECT_ROOT_DIR ) )

class EntireExportWorker( Worker ):
    sub_workers = { 'config' :ConfigWorker() }
    
    app_name = PositionOption( 1 )
    
    def execute( self ):
        export( self.app_name )
        
class TemplatesExportWorker( EntireExportWorker ):
    sub_workers = { 'config' :ConfigWorker() }
    
    app_name = PositionOption( 1 )
    
    def execute( self ):
        export_templates( self.app_name )

class MainDispatcher( Dispatcher ):
    entire = EntireExportWorker()
    templates = TemplatesExportWorker()

if __name__ == '__main__':
    dispatcher = MainDispatcher()
    dispatcher.dispatch( sys.argv[ 1: ] )