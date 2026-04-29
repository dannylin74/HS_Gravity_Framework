using System;
using System.Runtime.InteropServices;
using System.IO.MemoryMappedFiles;
using Vortice.Direct3D;
using Vortice.Direct3D11;
using Vortice.DXGI;
using Vortice.Mathematics;

namespace SovereignPerception
{
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct FrameHeader
    {
        public uint Width;
        public uint Height;
        public uint ActiveBuffer; // 0 or 1
        public long FrameIndex;
        public int Ready; // 1 = Ready, 0 = Writing
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("[HSGF_Nerve] Sovereign Perception Engine V1.3 (Fixed Alignment) Starting...");
            while (true)
            {
                try { RunNerve(); }
                catch (Exception ex) {
                    Console.WriteLine($"[Error] Nerve Collapse: {ex.Message}. Rebooting...");
                    System.Threading.Thread.Sleep(1000);
                }
            }
        }

        static void RunNerve()
        {
            if (D3D11.D3D11CreateDevice(null, DriverType.Hardware, DeviceCreationFlags.None, null, out ID3D11Device device).Failure) return;

            using var dxgiDevice = device.QueryInterface<IDXGIDevice>();
            using var adapter = dxgiDevice.GetAdapter();
            adapter.EnumOutputs(0, out var output).CheckError();
            using var output1 = output.QueryInterface<IDXGIOutput1>();

            IDXGIOutputDuplication duplication = output1.DuplicateOutput(device);
            var desc = output.Description;
            uint width = (uint)(desc.DesktopCoordinates.Right - desc.DesktopCoordinates.Left);
            uint height = (uint)(desc.DesktopCoordinates.Bottom - desc.DesktopCoordinates.Top);
            
            Console.WriteLine($"[HSGF_Nerve] Active: {width}x{height}");

            var stagingDesc = new Texture2DDescription {
                Width = width, Height = height, MipLevels = 1, ArraySize = 1,
                Format = Format.B8G8R8A8_UNorm, SampleDescription = new SampleDescription(1, 0),
                Usage = ResourceUsage.Staging, BindFlags = BindFlags.None,
                CPUAccessFlags = CpuAccessFlags.Read
            };
            using var staging = device.CreateTexture2D(stagingDesc);

            // Alignment Corrected Memory Setup
            long rowSize = width * 4;
            long frameSize = rowSize * height;
            long headerSize = 128; // Standardized header offset
            long totalSize = headerSize + frameSize;
            
            // Name must match Python: SovereignNerveLink
            using var mmf = MemoryMappedFile.CreateOrOpen("SovereignNerveLink", totalSize);
            using var accessor = mmf.CreateViewAccessor();

            long frameIdx = 0;
            while (true)
            {
                if (duplication.AcquireNextFrame(100, out var frameInfo, out var desktopResource).Success)
                {
                    using (var texture = desktopResource.QueryInterface<ID3D11Texture2D>()) {
                        device.ImmediateContext.CopyResource(staging, texture);
                    }
                    duplication.ReleaseFrame();

                    var mapped = device.ImmediateContext.Map(staging, 0, MapMode.Read, Vortice.Direct3D11.MapFlags.None);
                    unsafe
                    {
                        byte* srcPtr = (byte*)mapped.DataPointer;
                        byte* destPtr = null;
                        accessor.SafeMemoryMappedViewHandle.AcquirePointer(ref destPtr);
                        
                        // Header
                        FrameHeader* header = (FrameHeader*)destPtr;
                        header->Ready = 0;

                        // Row-by-Row Copy (The Fix)
                        byte* bufferBase = destPtr + headerSize;
                        for (int y = 0; y < height; y++)
                        {
                            Buffer.MemoryCopy(
                                srcPtr + (y * mapped.RowPitch), 
                                bufferBase + (y * rowSize), 
                                rowSize, rowSize
                            );
                        }

                        header->Width = width;
                        header->Height = height;
                        header->FrameIndex = frameIdx++;
                        header->Ready = 1;

                        accessor.SafeMemoryMappedViewHandle.ReleasePointer();
                    }
                    device.ImmediateContext.Unmap(staging, 0);
                    if (frameIdx % 60 == 0) Console.Write(".");
                }
            }
        }
    }
}
