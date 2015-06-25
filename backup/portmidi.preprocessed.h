# 1 "include/portmidi.h"
# 1 "<built-in>" 1
# 1 "<built-in>" 3
# 321 "<built-in>" 3
# 1 "<command line>" 1
# 1 "<built-in>" 2
# 1 "include/portmidi.h" 2
# 108 "include/portmidi.h"
 typedef int int32_t;
 typedef unsigned int uint32_t;
# 128 "include/portmidi.h"
typedef enum {
    pmNoError = 0,
    pmNoData = 0,
    pmGotData = 1,
    pmHostError = -10000,
    pmInvalidDeviceId,




    pmInsufficientMemory,
    pmBufferTooSmall,
    pmBufferOverflow,
    pmBadPtr,



    pmBadData,
    pmInternalError,
    pmBufferMaxSize

} PmError;





         PmError Pm_Initialize( void );





         PmError Pm_Terminate( void );



typedef void PortMidiStream;
# 182 "include/portmidi.h"
         int Pm_HasHostError( PortMidiStream * stream );






         const char *Pm_GetErrorText( PmError errnum );





         void Pm_GetHostErrorText(char * msg, unsigned int len);
# 207 "include/portmidi.h"
typedef int PmDeviceID;

typedef struct {
    int structVersion;
    const char *interf;
    const char *name;
    int input;
    int output;
    int opened;

} PmDeviceInfo;


         int Pm_CountDevices( void );
# 263 "include/portmidi.h"
         PmDeviceID Pm_GetDefaultInputDeviceID( void );

         PmDeviceID Pm_GetDefaultOutputDeviceID( void );





typedef int32_t PmTimestamp;
typedef PmTimestamp (*PmTimeProcPtr)(void *time_info);
# 289 "include/portmidi.h"
         const PmDeviceInfo* Pm_GetDeviceInfo( PmDeviceID id );
# 355 "include/portmidi.h"
         PmError Pm_OpenInput( PortMidiStream** stream,
                PmDeviceID inputDevice,
                void *inputDriverInfo,
                int32_t bufferSize,
                PmTimeProcPtr time_proc,
                void *time_info );

         PmError Pm_OpenOutput( PortMidiStream** stream,
                PmDeviceID outputDevice,
                void *outputDriverInfo,
                int32_t bufferSize,
                PmTimeProcPtr time_proc,
                void *time_info,
                int32_t latency );
# 436 "include/portmidi.h"
         PmError Pm_SetFilter( PortMidiStream* stream, int32_t filters );
# 454 "include/portmidi.h"
         PmError Pm_SetChannelMask(PortMidiStream *stream, int mask);
# 464 "include/portmidi.h"
         PmError Pm_Abort( PortMidiStream* stream );






         PmError Pm_Close( PortMidiStream* stream );
# 496 "include/portmidi.h"
PmError Pm_Synchronize( PortMidiStream* stream );
# 514 "include/portmidi.h"
typedef int32_t PmMessage;
# 580 "include/portmidi.h"
typedef struct {
    PmMessage message;
    PmTimestamp timestamp;
} PmEvent;
# 615 "include/portmidi.h"
         int Pm_Read( PortMidiStream *stream, PmEvent *buffer, int32_t length );





         PmError Pm_Poll( PortMidiStream *stream);
# 636 "include/portmidi.h"
         PmError Pm_Write( PortMidiStream *stream, PmEvent *buffer, int32_t length );







         PmError Pm_WriteShort( PortMidiStream *stream, PmTimestamp when, int32_t msg);




         PmError Pm_WriteSysEx( PortMidiStream *stream, PmTimestamp when, unsigned char *msg);
