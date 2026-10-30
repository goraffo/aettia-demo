"""
Funciones para construir cláusulas WHERE dinámicamente (con parámetros seguros).
"""


def _construir_filtros_comunes(
    pais=None,
    zona=None,
    skill=None,
    fecha_desde=None,
    fecha_hasta=None,
    params_dict=None
):
    """Construye los filtros comunes (país, zona, skill, fechas de captura)."""
    filtros = []
    
    if pais and pais != "Todos":
        filtros.append("pais = :pais")
        params_dict['pais'] = pais
    
    if zona == "Capital":
        filtros.append("""(
            (pais = 'Peru' AND ubicacion ILIKE '%Lima%') OR
            (pais = 'Chile' AND ubicacion ILIKE '%Santiago%') OR
            (pais = 'Argentina' AND ubicacion ILIKE '%Buenos Aires%')
        )""")
    elif zona == "Provincias":
        filtros.append("""NOT (
            (pais = 'Peru' AND ubicacion ILIKE '%Lima%') OR
            (pais = 'Chile' AND ubicacion ILIKE '%Santiago%') OR
            (pais = 'Argentina' AND ubicacion ILIKE '%Buenos Aires%')
        )""")
    
    if fecha_desde:
        periodo_desde = int(fecha_desde[:4]) * 100 + int(fecha_desde[5:7])
        filtros.append("(c_yr * 100 + CAST(c_mes AS INTEGER)) >= :periodo_desde")
        params_dict['periodo_desde'] = periodo_desde
    if fecha_hasta:
        periodo_hasta = int(fecha_hasta[:4]) * 100 + int(fecha_hasta[5:7])
        filtros.append("(c_yr * 100 + CAST(c_mes AS INTEGER)) <= :periodo_hasta")
        params_dict['periodo_hasta'] = periodo_hasta
    
    return filtros


def construir_filtros_puestos(
    puestos=None,
    pais=None,
    zona=None,
    skill=None,
    dominio=None,
    fecha_desde=None,
    fecha_hasta=None,
    params_dict=None
):
    """Construye cláusula WHERE para la vista PUESTOS."""
    if params_dict is None:
        params_dict = {}
    
    filtros = []
    
    if puestos:
        condiciones = []
        for i, p in enumerate(puestos):
            key = f"puesto_{i}"
            condiciones.append(f"unaccent(c_titulo) ILIKE unaccent(:{key})")
            params_dict[key] = f"%{p}%"
        filtros.append(f"({' OR '.join(condiciones)})")
    
    if dominio and dominio != "Todos":
        filtros.append("dominio = :dominio")
        params_dict['dominio'] = dominio
    
    filtros.extend(_construir_filtros_comunes(
        pais=pais,
        zona=zona,
        skill=skill,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        params_dict=params_dict
    ))
    
    where = " AND ".join(filtros) if filtros else "1=1"
    return where, params_dict


def construir_filtros_dominios(
    dominios=None,
    pais=None,
    zona=None,
    skill=None,
    fecha_desde=None,
    fecha_hasta=None,
    params_dict=None
):
    """Construye cláusula WHERE para la vista DOMINIOS."""
    if params_dict is None:
        params_dict = {}
    
    filtros = []
    
    if dominios:
        condiciones = []
        for i, d in enumerate(dominios):
            key = f"dominio_{i}"
            condiciones.append(f"dominio = :{key}")
            params_dict[key] = d
        filtros.append(f"({' OR '.join(condiciones)})")
    
    filtros.extend(_construir_filtros_comunes(
        pais=pais,
        zona=zona,
        skill=skill,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        params_dict=params_dict
    ))
    
    where = " AND ".join(filtros) if filtros else "1=1"
    return where, params_dict


def construir_filtros_escuelas(
    organizaciones=None,
    dominio=None,
    tipos=None,
    skills=None,
    fecha_desde=None,
    fecha_hasta=None,
    params_dict=None
):
    """Construye cláusula WHERE para la vista ESCUELAS."""
    if params_dict is None:
        params_dict = {}
    
    filtros = []
    
    if organizaciones:
        condiciones = []
        for i, org in enumerate(organizaciones):
            key = f"org_{i}"
            condiciones.append(f"pm.id_org = :{key}")
            params_dict[key] = org
        filtros.append(f"({' OR '.join(condiciones)})")
    
    if dominio is not None:
        filtros.append("pm.id_dominio = :dominio")
        params_dict['dominio'] = dominio
    
    if tipos:
        condiciones = []
        for i, t in enumerate(tipos):
            key = f"tipo_{i}"
            condiciones.append(f"pm.tipo = :{key}")
            params_dict[key] = t
        filtros.append(f"({' OR '.join(condiciones)})")
    
    if skills:
        condiciones = []
        for i, s in enumerate(skills):
            key = f"skill_{i}"
            condiciones.append(f"pm.c_producto ILIKE :{key}")
            params_dict[key] = f"%{s}%"
        filtros.append(f"({' OR '.join(condiciones)})")
    
    where = " AND ".join(filtros) if filtros else "1=1"
    return where, params_dict


def construir_filtros_tipos(
    tipos=None,
    dominio=None,
    skills=None,
    origen=None,
    params_dict=None
):
    """Construye cláusula WHERE para la vista TIPOS."""
    if params_dict is None:
        params_dict = {}
    
    filtros = []
    
    if tipos:
        condiciones = []
        for i, t in enumerate(tipos):
            key = f"tipo_{i}"
            condiciones.append(f"pm.tipo = :{key}")
            params_dict[key] = t
        filtros.append(f"({' OR '.join(condiciones)})")
    
    if dominio is not None:
        filtros.append("pm.id_dominio = :dominio")
        params_dict['dominio'] = dominio
    
    if skills:
        condiciones = []
        for i, s in enumerate(skills):
            key = f"skill_{i}"
            condiciones.append(f"pm.c_producto ILIKE :{key}")
            params_dict[key] = f"%{s}%"
        filtros.append(f"({' OR '.join(condiciones)})")
    
    if origen and origen != "Todos":
        if origen == "Peruano":
            filtros.append("pm.origen = 'INDEX'")
        elif origen == "Extranjero":
            filtros.append("pm.origen = 'EDEC'")
    
    where = " AND ".join(filtros) if filtros else "1=1"
    return where, params_dict


def construir_filtros_skills(
    skills_buscadas=None,
    pais=None,
    zona=None,
    dominio=None,
    fecha_desde=None,
    fecha_hasta=None,
    params_dict=None
):
    """Construye cláusula WHERE para la vista SKILLS (Analista de Talento)."""
    if params_dict is None:
        params_dict = {}
    
    filtros = []
    
    if skills_buscadas:
        condiciones = []
        for i, s in enumerate(skills_buscadas):
            key = f"skl_{i}"
            condiciones.append(f"(unaccent(c_titulo) ILIKE unaccent(:{key}) OR unaccent(c_detalle) ILIKE unaccent(:{key}))")
            params_dict[key] = f"%{s}%"
        filtros.append(f"({' OR '.join(condiciones)})")
    
    if dominio and dominio != "Todos":
        filtros.append("dominio = :dominio")
        params_dict['dominio'] = dominio
    
    filtros.extend(_construir_filtros_comunes(
        pais=pais,
        zona=zona,
        skill=None,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        params_dict=params_dict
    ))
    
    where = " AND ".join(filtros) if filtros else "1=1"
    return where, params_dict


def construir_filtros_skills_dc(
    skills_buscadas=None,
    dominio_id=None,
    tipos=None,
    origen=None,
    fecha_desde=None,
    fecha_hasta=None,
    params_dict=None
):
    """Construye cláusula WHERE para la vista SKILLS (Diseñador Curricular)."""
    if params_dict is None:
        params_dict = {}
    
    filtros = []
    
    if skills_buscadas:
        condiciones = []
        for i, s in enumerate(skills_buscadas):
            key = f"dcs_{i}"
            condiciones.append(f"pm.c_producto ILIKE :{key}")
            params_dict[key] = f"%{s}%"
        filtros.append(f"({' OR '.join(condiciones)})")
    
    if dominio_id is not None:
        filtros.append("pm.id_dominio = :dominio")
        params_dict['dominio'] = dominio_id
    
    if tipos:
        condiciones = []
        for i, t in enumerate(tipos):
            key = f"tipo_{i}"
            condiciones.append(f"pm.tipo = :{key}")
            params_dict[key] = t
        filtros.append(f"({' OR '.join(condiciones)})")
    
    if origen and origen != "Todos":
        if origen == "Peruano":
            filtros.append("pm.origen = 'INDEX'")
        elif origen == "Extranjero":
            filtros.append("pm.origen = 'EDEC'")
    
    where = " AND ".join(filtros) if filtros else "1=1"
    return where, params_dict