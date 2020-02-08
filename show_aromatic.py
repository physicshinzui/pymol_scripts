

def get_res_resi(obj):
    my_dict = { 'my_list' : [] }
    cmd.iterate(f"{obj} and resname Phe+Tyr+Trp+His and name ca","my_list.append((resi,resn))",space=my_dict)
    return list(my_dict['my_list'])

def show_aroma():
   objs = cmd.get_object_list('all') 
   for obj in objs:
       selection = f'{obj} and resname Phe+Tyr+Trp+His'

       #show aroma
       cmd.select(f'{obj}_aroma', selection)
       cmd.show('sticks', f'{obj}_aroma')

       #measure distances between aromas and show these
       residues = get_res_resi(obj)
       n = len(residues)
       print(residues, n)
       for i in range(n):
          cmd.pseudoatom('center1', f'resid {residues[i][0]} and name cg+cd*+cz+ce*')
          for j in range(i+1, n-1):
              print(residues[i],residues[j])
              cmd.pseudoatom('center2', f'resid {residues[j][0]} and name cg+cd*+cz+ce*')

              cmd.distance(f'stacking_{obj}', 
                           f'center1', 
                           f'center2', 
                           mode=3, cutoff=6.0)
              cmd.delete('center2')
          cmd.delete('center1')

       #show center of mass for each aromatic residues
       for i in range(n):
          cmd.pseudoatom('centers', f'resid {residues[i][0]} and name cg+cd*+cz+ce*')

cmd.extend('aroma', show_aroma)
