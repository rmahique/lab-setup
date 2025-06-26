#!/usr/bin/python3
#
# Authors: Raul Mahiques
# License: GPLv3
# 
# $Id$
#

from xmlrpc.client import ServerProxy
import ssl, argparse, yaml



def smlm_login(server, user, pwd):
  """
  Performs an authentication login and returns the session key
  """
  context = ssl._create_unverified_context()
  client = ServerProxy('https://' + server + '/rpc/api', context=context)
  key = client.auth.login(user, pwd)
  return key, client


def smlm_logout(key, client):
  """
  Performs a logout
  """
  client.auth.logout(key)


def smlm_create_ak(key, client, name, description, baseChannelLabel, usageLimit, entitlements , universalDefault, appstreams, childchannels, configchannels, packages, servergroups):
key, client, inputparam.akname, inputparam.description, inputparam.basechannellabel or '', inputparam.usagelimit or 0, inputparam.entitlements or '', inputparam.universal or False, inputparam.appstreams or '', inputparam.childchannels or '', inputparam.configchannels or '', inputparam.packages or '', inputparam.servergroups or ''

  """
  Creates an activation key in SMLM
  """
  systems = client.activationkey.create(key, name, description, baseChannelLable, usageLimit, entitlements , universalDefault)


def smlm_get_ak(key, client, akname):
  """
  Returns information about an Activation Key in SMLM
  """
  print(yaml.dump(lient.activationkey.getDetails(key, akname)))
  

def smlm_list_aks(key, client):
  """
  Returns the list of Activation Key in SMLM
  """
  return client.activationkey.listActivationKeys(key)


def smlm_get_akid(key, client, akname):
  """
  Retrieves information about a SMLM Activation Key and returns the Activation Key ID.
  """
  akDetails = client.activationkey.getDetails(key, akname)
  return akDetails['id']


def smlm_del_ak(key, client, akid):
  """
  Deletes an Activation Key from SMLM
  """
  print(akid)
  result = client.activationkey.delete(key, akid)
  print(result)


def main():
  """
  Main function that parses the command-line arguments and initiate the API calls.
  """
  # Define how we want to process command line arguments
  parser = argparse.ArgumentParser(prog='smlm_ak',description='Manages SMLM Activation keys')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-a','--add', action='store_true', help='Add Activation Key')
  group.add_argument('-d','--delete', action='store_true', help='Delete Activation Keys')
  group.add_argument('-g','--get', action='store_true', help='Retrieve Activation Keys information')
  group.add_argument('-l','--list', action='store_true', help='List Activation Keys')
  parser.add_argument('-u', '--user', type=str, required=True, help='User name with privileges to create Activation Keys')
  parser.add_argument('-p', '--pwd', type=str, required=True, help='Password for user')
  parser.add_argument('-s', '--server', type=str, required=True, help='Server FQDN')
  parser.add_argument('-k','--akname', type=str, help='Activation Keys name. Must meet same criteria as in the web UI.')
  parser.add_argument('--description', type=str, help='Activation Key description.')
  parser.add_argument('--basechannellabel', type=str, help='Base Channel Label.')
  parser.add_argument('--usagelimit', type=int, help="Number of systems that can use this, leave it empty for unlimited")
  parser.add_argument('--entitlements', type=str, help="Entitlements separated by comma: container_build_host,monitoring_entitled,osimage_build_host,virtualization_host,ansible_control_node,proxy_entitled,")
  parser.add_argument('--universal', action='store_true', help='Makes this activation key the universal default.')
  parser.add_argument('--appstreams', type=str, help='Add app streams to an activation key. Separated by comma: aa,bb,cc')
  parser.add_argument('--childchannels', type=str, help='Add child channels to an activation key. Separated by comma: aa,bb,cc')
  parser.add_argument('--configchannels', type=str, help='Add configuration channels to an activation key. Separated by comma: aa,bb,cc')
  parser.add_argument('--packages', type=str, help='Add packages to an activation key. Separated by comma: aa,bb,cc')
  parser.add_argument('--servergroups', type=str, help='Add server groups to an activation key. Separated by comma: aa,bb,cc')
  parser.add_argument('--debug', action='store_true', help="Use it to enable debug messages.")
  inputparam=parser.parse_args()

  context = ssl._create_unverified_context()
  client = ServerProxy('https://' + inputparam.server + '/rpc/api', context=context)

  key, client = smlm_login(inputparam.server, inputparam.user, inputparam.pwd)

  if(inputparam.add and inputparam.akname and inputparam.description and inputparam.basechannellabel):
    print("We add " + str(inputparam.akname))
    smlm_create_ak(key, client, inputparam.akname, inputparam.description, inputparam.basechannellabel or '', inputparam.usagelimit or 0, inputparam.entitlements or '', inputparam.universal or False, inputparam.appstreams or '', inputparam.childchannels or '', inputparam.configchannels or '', inputparam.packages or '', inputparam.servergroups or '')
  elif(inputparam.delete):
    print("We delete " + str(inputparam.akname))
    akid=smlm_get_akid(key, client, inputparam.akname)
    smlm_del_ak(key, client, akid)
  elif(inputparam.get):
    print("We retrive information about: " + str(inputparam.akname))
    print(str(smlm_get_ak(key, client, inputparam.akname)))
  elif(inputparam.list):
    print("We are retrieving the list of Activation Keys")
    print(yaml.dump(smlm_list_aks(key, client)))
  else:
    print("Invalid or missing parameters")
    if(inputparam.debug):
      print(yaml.dump(inputparam))

  smlm_logout(key, client)



if __name__ == '__main__':
  main()




