# Migrar VM de VirtualBox a VMware Workstation

> Guía paso a paso para migrar máquinas virtuales entre los dos hypervisores más usados en laboratorios de ciberseguridad.

---

## 1. Por qué migrar

| VirtualBox | VMware Workstation |
|-----------|-------------------|
| Gratuito | De pago (licencia educativa) |
| Rendimiento general | Mejor rendimiento con USB 3.0, tarjetas de red, 3D |
| Menos opciones de snapshots | Snapshots más fiables |
| Compatibilidad amplia | Mejor soporte de VMs de laboratorio (HTB, TryHackMe) |

---

## 2. Método exportar/importar (recomendado)

### Paso 1: Exportar desde VirtualBox

1. Apagar la VM
2. Seleccionar la VM → **Archivo** → **Exportar appliance**
3. Seleccionar formato **OVF 1.0**
4. Configurar opciones de exportación
5. Guardar el archivo `.ovf` o `.ova`

### Paso 2: Importar en VMware

1. Abrir VMware Workstation
2. **Archivo** → **Open** → seleccionar el archivo `.ovf` o `.ova`
3. Asignar nombre y ubicación
4. VMware convertirá el formato automáticamente
5. Encender la VM y verificar que funciona

---

## 3. Método conversión directa de disco

### Paso 1: Obtener el disco virtual de VirtualBox

```bash
# El disco está en:
# Windows: C:\Users\_usuario\VirtualBox VMs\nombre_vm\nombre_vm.vdi
# Linux: ~/VirtualBox VMs/nombre_vm/nombre_vm.vdi
```

### Paso 2: Convertir el disco con qemu-img

```bash
# Instalar qemu-img (si no está)
# Windows: descargar QEMU
# Linux:
sudo apt install qemu-utils

# Convertir VDI a VMDK
qemu-img convert -f vdi -O vmdk nombre_vm.vdi nombre_vm.vmdk
```

### Paso 3: Crear VM en VMware con disco existente

1. Crear nueva VM en VMware
2. Seleccionar **"Use an existing virtual disk"**
3. Seleccionar el archivo `.vmdk` generado
4. Configurar RAM, CPU y red
5. Encender y verificar

---

## 4. Método manual (avanzado)

### Exportar desde VirtualBox con VBoxManage

```bash
# Exportar a OVF
VBoxManage export "Nombre VM" -o nombre_vm.ovf

# Convertir disco
VBoxManage clonehd nombre_vm.vdi nombre_vm.vmdk --format VMDK
```

### Importar en VMware

```bash
# Usar vmware-vdiskmanager para optimizar
vmware-vdiskmanager -r nombre_vm.vmdk -t 0 nombre_vm_optimizado.vmdk
```

---

## 5. Configuración post-migración

### Verificar controladores

- **VMware Tools**: Instalar para mejor rendimiento (drag & drop, clipboard compartido)
- **Adaptador de red**: Cambiar a桥接 o NAT según necesidad
- **USB**: Configurar filtrados USB si es necesario

### Solucionar problemas comunes

| Problema | Solución |
|----------|----------|
| VM no arranca | Revisar configuración de BIOS/UEFI en VMware |
| Sin red | Cambiar adaptador de red a桥接 o NAT |
| Pantalla pequeña | Instalar VMware Tools |
| USB no funciona | Configurar filtrados USB en VMware |
| Snapshots no funcionan | Recrear snapshots en VMware |

---

## 6. Diferencias importantes

| Característica | VirtualBox | VMware |
|---------------|-----------|--------|
| Formato de disco | VDI | VMDK |
| Formato de exportación | OVF/OVA | OVF/OVA |
| Snapshot limit | Sin límite práctico | Sin límite práctico |
| Clonación | Rápida (linked clone) | Rápida (linked clone) |
| Red |桥接, NAT, Host-Only |桥接, NAT, Host-Only |
| USB | 1.1/2.0/3.0 | 1.1/2.0/3.0/3.1 |

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

> #virtualbox #vmware #vm #lab #configuracion
